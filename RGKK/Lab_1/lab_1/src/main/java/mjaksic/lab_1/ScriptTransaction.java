package mjaksic.lab_1;

import com.google.common.collect.ImmutableSet;
import org.bitcoinj.core.*;
import org.bitcoinj.crypto.TransactionSignature;
import org.bitcoinj.script.Script;
import org.bitcoinj.wallet.SendRequest;
import org.bitcoinj.wallet.Wallet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.spongycastle.util.encoders.Hex;

public abstract class ScriptTransaction implements AutoCloseable {

    private final static Logger LOGGER = LoggerFactory.getLogger(ScriptTransaction.class);

    private final WalletKit walletKit;
    private final NetworkParameters parameters;

    public ScriptTransaction(WalletKit walletKit, NetworkParameters parameters) {
        this.parameters = parameters;
        this.walletKit = walletKit;
    }

    public Wallet getWallet() {
        return walletKit.getWallet();
    }

    public abstract Script createLockingScript();

    public abstract Script createUnlockingScript(Transaction unsignedTransaction);

    protected TransactionSignature sign(Transaction transaction, ECKey key) {
        Script script = transaction.getInput(0).getConnectedOutput().getScriptPubKey();
        return transaction.calculateSignature(0, key, script, Transaction.SigHash.ALL, false);
    }


    public void testScript(Script lockingScript, Script spendingScript,Transaction unlockingTransaction) {
        spendingScript.correctlySpends(unlockingTransaction, 0, lockingScript, ImmutableSet.of(Script.VerifyFlag.P2SH));
    }

    public Transaction createOutgoingTransaction(Script script, Coin amount) throws InsufficientMoneyException {
        Transaction transaction = new Transaction(parameters);
        transaction.addOutput(amount, script);
        SendRequest request = SendRequest.forTx(transaction);
        walletKit.getWallet().completeTx(request);
        return transaction;
    }


    public Transaction createUnsignedUnlockingTransaction(TransactionOutput output, Address receiveAddress) {
        Transaction transaction = new Transaction(parameters);
        transaction.addOutput(output.getValue().subtract(Coin.MILLICOIN.multiply(2)), receiveAddress);
        transaction.addInput(output);
        return transaction;
    }

    public void sendTransaction(Transaction transaction) {
        LOGGER.info("Transaction hex you can directly submit this to a block explorer:\n{}", new String(Hex.encode(transaction.bitcoinSerialize())));
        walletKit.getWallet().commitTx(transaction);
        walletKit.getPeerGroup().broadcastTransaction(transaction);
        LOGGER.info("Broadcasted transaction: {}", transaction.getHashAsString());

    }

    /**
     * @return a random ECKey that hasn't yet been added to the wallet
     */
    public ECKey randKey() {
        return new ECKey();
    }

    public void importKey(ECKey key) {
        getWallet().importKey(key);
    }

    public Address getReceiveAddress() {
        return getWallet().currentReceiveAddress();
    }

    protected NetworkParameters getParameters() {
        return parameters;
    }

    @Override
    public void close() {
        walletKit.close();
    }
}
