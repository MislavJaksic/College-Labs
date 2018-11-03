package mjaksic.lab_1;

import org.bitcoinj.core.ECKey;
import org.bitcoinj.core.NetworkParameters;
import org.bitcoinj.core.Transaction;
import org.bitcoinj.crypto.TransactionSignature;
import org.bitcoinj.script.Script;
import org.bitcoinj.script.ScriptBuilder;

import static org.bitcoinj.script.ScriptOpCodes.OP_CHECKSIG;

/**
 * This class represents Pay-2-Public-Key type of bitcoin transaction.
 * Every transaction consists of 2 parts:
 * <ul>
 *     <li>Inputs (unlocking scripts)</li>
 *     <li>Outputs (locking scripts)</li>
 * </ul>
 * Pay-2-Public-Key defines those two parts as:
 * <pre>
 *  Locking script = &lt;public key&gt; OP_CHECKSIG
 *  Unlocking script = &lt;signature(key)&gt;
 * </pre>
 *
 * For more information about how Bitcoin transactions work
 * look in publicly available book "Mastering Bitcoin" chapter 7
 * by following this
 * <a href="https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch06.asciidoc">link </a>.
 */
public class PayToPubKey extends ScriptTransaction {

    // Key used to create destination address of a transaction.
    private final ECKey key;

    public PayToPubKey(WalletKit walletKit, NetworkParameters parameters) {
        super(walletKit, parameters);
        // Create new wallet key that is going to be used to send btc
        // to yourself. Wallet can have as many keys (addresses) as you want.
        // Wallets usually use "Deterministic" keys to generate hierarchy of keys
        // for easier key management.
        key = getWallet().freshReceiveKey();
    }

    @Override
    public Script createLockingScript() {
        return new ScriptBuilder()     // Create new ScriptBuilder object that builds locking script
                .data(key.getPubKey()) // Add public key to the locking script
                .op(OP_CHECKSIG)       // Add OP_CHECKSIG to the locking script
                .build();              // Build "<pubKey> OP_CHECKSIG" locking script
    }

    @Override
    public Script createUnlockingScript(Transaction unsignedTransaction) {
        TransactionSignature txSig = sign(unsignedTransaction, key); // Create key signature
        return new ScriptBuilder()                                   // Create new ScriptBuilder
                .data(txSig.encodeToBitcoin())                       // Add key signature to unlocking script
                .build();                                            // Build "<signature(key)>" unlocking script
    }
}
