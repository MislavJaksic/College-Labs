package mjaksic.lab_1.task_2;

import static org.bitcoinj.script.ScriptOpCodes.OP_2DUP;
import static org.bitcoinj.script.ScriptOpCodes.OP_SWAP;
import static org.bitcoinj.script.ScriptOpCodes.OP_SUB;
import static org.bitcoinj.script.ScriptOpCodes.OP_EQUAL;
import static org.bitcoinj.script.ScriptOpCodes.OP_ROT;
import static org.bitcoinj.script.ScriptOpCodes.OP_GREATERTHAN;
import static org.bitcoinj.script.ScriptOpCodes.OP_ADD;

import org.bitcoinj.core.NetworkParameters;
import org.bitcoinj.core.Transaction;
import org.bitcoinj.script.Script;
import org.bitcoinj.script.ScriptBuilder;

import mjaksic.lab_1.ScriptTransaction;
import mjaksic.lab_1.WalletKit;

/**
 * You must implement locking and unlocking script such that transaction output is locked by 2 integers x and y
 * such that they are solution to the equation system:
 * <pre>
 *     x + y = first four digits of your student id
 *     abs(x-y) = last four digits of your student id
 * </pre>
 * If needed change last digit of your student id such that x and y have same parity. This is needed so that equation
 * system has integer solutions.
 */
public class LinearEquationTransaction extends ScriptTransaction {

    public LinearEquationTransaction(WalletKit walletKit, NetworkParameters parameters) {
        super(walletKit, parameters);
    }

    @Override
    public Script createLockingScript() {
    	int last_four_digits = 1622;
    	int first_four_digits = 36;
    	int logic_zero = 0;
    	int logic_two = 2;
    	
    	return new ScriptBuilder()
    			.op(OP_2DUP)
    			.op(OP_2DUP)
    			.op(OP_SWAP)
    			.op(OP_SUB)
    			.number(last_four_digits)
    			.op(OP_EQUAL)
    			.op(OP_ROT)
    			.op(OP_ROT)
    			.op(OP_SUB)
    			.number(last_four_digits)
    			.op(OP_EQUAL)
    			.op(OP_ADD)
    			.number(logic_zero)
    			.op(OP_GREATERTHAN)
    			.op(OP_ROT)
    			.op(OP_ROT)
    			.op(OP_ADD)
    			.number(first_four_digits)
    			.op(OP_EQUAL)
    			.op(OP_ADD)
    			.number(logic_two)
    			.op(OP_EQUAL)
    			
                .build();
    }

    @Override
    public Script createUnlockingScript(Transaction unsignedScript) {
    	/**
    	int x = -793; //correct
    	int y = 829;
    	*/
    	
    	int x = 829; //correct
    	int y = -793;
    	
    	/**
    	int x = 827; //wrong
    	int y = -1155;
    	*/
    	
    	return new ScriptBuilder()       
                .number(x)
                .number(y)
                .build();
    }
}
