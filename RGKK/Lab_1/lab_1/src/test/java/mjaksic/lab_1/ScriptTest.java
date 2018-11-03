package mjaksic.lab_1;

import org.bitcoinj.core.*;
import org.bitcoinj.params.RegTestParams;
import org.bitcoinj.script.Script;
import org.junit.Assert;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import mjaksic.lab_1.task_1.PayToPubKeyHash;
import mjaksic.lab_1.task_2.LinearEquationTransaction;
import mjaksic.lab_1.task_3.MultiSigTransaction;

import java.io.File;

public class ScriptTest {

    private WalletKit walletKit;
    private NetworkParameters networkParameters;

    private static final Logger LOGGER = LoggerFactory.getLogger(ScriptTest.class);

    public ScriptTest() {
        String walletName = "wallet";
        this.networkParameters = RegTestParams.get();
        this.walletKit = new WalletKit(networkParameters, new File(walletName), "password");
    }

    @Test
    public void printAddress() {
        LOGGER.info("Importing key");
        LOGGER.info("Your address is {}", walletKit.getWallet().currentReceiveAddress());
        LOGGER.info("Your balance is {}", walletKit.getWallet().getBalance());
        walletKit.close();
    }

    private void testTransaction(ScriptTransaction scriptTransaction) throws InsufficientMoneyException {
        Script lockingScript = scriptTransaction.createLockingScript();
        Transaction transaction = scriptTransaction.createOutgoingTransaction(lockingScript, Coin.CENT);
        transaction.getOutputs().stream()
                .filter(to -> to.getScriptPubKey().equals(lockingScript))
                .findAny()
                .ifPresent(relevantOutput -> {
                    Transaction unlockingTransaction = scriptTransaction.createUnsignedUnlockingTransaction(relevantOutput, scriptTransaction.getReceiveAddress());
                    Script unlockingScript = scriptTransaction.createUnlockingScript(unlockingTransaction);
                    scriptTransaction.testScript(lockingScript, unlockingScript, unlockingTransaction);
                    unlockingTransaction.getInput(0).setScriptSig(unlockingScript);
                    scriptTransaction.sendTransaction(transaction);
                    scriptTransaction.sendTransaction(unlockingTransaction);
                });
    }

    @Test
    public void testPayToPubKey() {
        try (ScriptTransaction payToPubKey = new PayToPubKey(walletKit, networkParameters)) {
            testTransaction(payToPubKey);
        } catch (Exception e) {
            e.printStackTrace();
            Assert.fail(e.getMessage());
        }
    }

    @Test
    public void testPayToPubKeyHash() {
        try (ScriptTransaction payToPubKeyHash = new PayToPubKeyHash(walletKit, networkParameters)) {
            testTransaction(payToPubKeyHash);
        } catch (Exception e) {
            e.printStackTrace();
            Assert.fail(e.getMessage());
        }
    }

    @Test
    public void testLinearEquation() {
        try (LinearEquationTransaction linEq = new LinearEquationTransaction(walletKit, networkParameters)) {
            testTransaction(linEq);
        } catch (Exception e) {
            e.printStackTrace();
            Assert.fail(e.getMessage());
        }
    }

    @Test
    public void testMultiSig() {
        try (ScriptTransaction multiSig = new MultiSigTransaction(walletKit, networkParameters)) {
            testTransaction(multiSig);
        } catch (Exception e) {
            e.printStackTrace();
            Assert.fail(e.getMessage());
        }
    }
}
