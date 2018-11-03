package mjaksic.lab_1.task_1;

import static org.bitcoinj.script.ScriptOpCodes.OP_CHECKSIG;
import static org.bitcoinj.script.ScriptOpCodes.OP_DUP;
import static org.bitcoinj.script.ScriptOpCodes.OP_HASH160;
import static org.bitcoinj.script.ScriptOpCodes.OP_EQUALVERIFY;

import org.bitcoinj.core.Address;
import org.bitcoinj.core.ECKey;
import org.bitcoinj.core.NetworkParameters;
import org.bitcoinj.core.Transaction;
import org.bitcoinj.crypto.TransactionSignature;
import org.bitcoinj.params.MainNetParams;
import org.bitcoinj.script.Script;
import org.bitcoinj.script.ScriptBuilder;

import mjaksic.lab_1.ScriptTransaction;
import mjaksic.lab_1.WalletKit;

/**
 * You must implement standard Pay-2-Public-Key-Hash transaction type.
 */
public class PayToPubKeyHash extends ScriptTransaction {
	
	private ECKey sender_keychain;
	private ECKey receiver_keychain;
	

    public PayToPubKeyHash(WalletKit walletKit, NetworkParameters parameters) {
        super(walletKit, parameters);
        
        this.SetSameKeyForSenderReceiver();
    }
    
    private void SetSameKeyForSenderReceiver() {
    	ECKey keychain = this.GetAdressKey();
    	this.sender_keychain = keychain;
    	this.receiver_keychain = keychain;
    }
    
    private ECKey GetAdressKey() {
    	return getWallet().freshReceiveKey();
    }

    
    
    @Override
    public Script createLockingScript() {
    	return new ScriptBuilder()
    			.op(OP_DUP)
    			.op(OP_HASH160)
                .data(this.GetReceiversHash160PublicKey())
                .op(OP_EQUALVERIFY)
                .op(OP_CHECKSIG)
                .build();
    }

    @Override
    public Script createUnlockingScript(Transaction unsignedTransaction) {
    	byte[] senders_signed_transaction = this.SignTransactionWithSendersKeychain(unsignedTransaction);
        return new ScriptBuilder()       
                .data(senders_signed_transaction)
                .data(this.GetReceiversPublicKey())
                .build();
    }
    
    
    
    private byte[] SignTransactionWithSendersKeychain(Transaction transaction) {
    	TransactionSignature signed_transaction = this.sign(transaction, this.sender_keychain);
    	return signed_transaction.encodeToBitcoin();
    }
    
    private byte[] GetReceiversPublicKey() {
    	return this.receiver_keychain.getPubKey();
    }
    
    private byte[] GetReceiversHash160PublicKey() {
    	NetworkParameters network_parameters = MainNetParams.get();
    	Address address = this.receiver_keychain.toAddress(network_parameters);
    	return address.getHash160();
    }
}
