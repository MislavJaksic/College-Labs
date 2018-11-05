package mjaksic.lab_1.task_3;

import static org.bitcoinj.script.ScriptOpCodes.OP_CHECKMULTISIG;
import static org.bitcoinj.script.ScriptOpCodes.OP_CHECKSIG;
import static org.bitcoinj.script.ScriptOpCodes.OP_ROT;
import static org.bitcoinj.script.ScriptOpCodes.OP_ADD;
import static org.bitcoinj.script.ScriptOpCodes.OP_EQUAL;

import org.bitcoinj.core.ECKey;
import org.bitcoinj.core.NetworkParameters;
import org.bitcoinj.core.Transaction;
import org.bitcoinj.crypto.TransactionSignature;
import org.bitcoinj.script.Script;
import org.bitcoinj.script.ScriptBuilder;

import mjaksic.lab_1.ScriptTransaction;
import mjaksic.lab_1.WalletKit;

/**
 * You must implement locking and unlocking script such that transaction output is locked by one mandatory authority
 * (e.g. bank) and at least 1 of 3 other authorities (e.g. bank associates).
 */
public class MultiSigTransaction extends ScriptTransaction {

	private ECKey trust_keychain;
	private ECKey client_A_keychain;
	private ECKey client_B_keychain;
	private ECKey client_C_keychain;
	
    public MultiSigTransaction(WalletKit walletKit, NetworkParameters parameters) {
        super(walletKit, parameters);
        
        this.SetSameKeyForSenderReceiver();
    }
    
    private void SetSameKeyForSenderReceiver() {
    	this.trust_keychain = this.GetAddressKey();
    	this.client_A_keychain = this.GetAddressKey();
    	this.client_B_keychain = this.GetAddressKey();
    	this.client_C_keychain = this.GetAddressKey();
    }
    
    private ECKey GetAddressKey() {
    	return getWallet().freshReceiveKey();
    }

    
    
    @Override
    public Script createLockingScript() {
    	int client_signatures_required = 1;
    	int total_client_signatures = 3;
    	int logical_two = 2;
    	
    	return new ScriptBuilder()
    			.data(this.GetPublicKeyFromKeychain(this.trust_keychain))
    			.op(OP_CHECKSIG)
    			.op(OP_ROT)
    			.op(OP_ROT)
    			.number(client_signatures_required)
    			.data(this.GetPublicKeyFromKeychain(this.client_A_keychain))
    			.data(this.GetPublicKeyFromKeychain(this.client_B_keychain))
    			.data(this.GetPublicKeyFromKeychain(this.client_C_keychain))
    			.number(total_client_signatures)
                .op(OP_CHECKMULTISIG)
                .op(OP_ADD)
                .number(logical_two)
                .op(OP_EQUAL)
                .build();
    }
    
    private byte[] GetPublicKeyFromKeychain(ECKey keychain) {
    	return keychain.getPubKey();
    }

    @Override
    public Script createUnlockingScript(Transaction unsignedTransaction) {
    	byte[] client_A_signed_transaction = this.SignTransactionWithKeychain(unsignedTransaction, this.client_A_keychain);
    	byte[] client_B_signed_transaction = this.SignTransactionWithKeychain(unsignedTransaction, this.client_B_keychain);
    	byte[] client_C_signed_transaction = this.SignTransactionWithKeychain(unsignedTransaction, this.client_C_keychain);
    	
    	byte[] trust_signed_transaction = this.SignTransactionWithKeychain(unsignedTransaction, this.trust_keychain);
    	
    	return new ScriptBuilder()       
    			.number(0) //DO NOT USE OP_0, IT WILL NOT WORK
    			.data(client_C_signed_transaction)
    			.data(trust_signed_transaction)
                .build();
    }
    
    private byte[] SignTransactionWithKeychain(Transaction transaction, ECKey keychain) {
    	TransactionSignature signed_transaction = this.sign(transaction, keychain);
    	return signed_transaction.encodeToBitcoin();
    }
}
