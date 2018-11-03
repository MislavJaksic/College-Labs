package mjaksic.lab_1;

import org.bitcoinj.core.NetworkParameters;
import org.bitcoinj.core.PeerAddress;
import org.bitcoinj.core.PeerGroup;
import org.bitcoinj.kits.WalletAppKit;
import org.bitcoinj.wallet.Wallet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.net.InetAddress;

public class WalletKit implements AutoCloseable {

    private final static Logger LOGGER = LoggerFactory.getLogger(WalletKit.class);

    private final WalletAppKit walletAppKit;

    public WalletKit(NetworkParameters parameters, File file, String password) {
        this.walletAppKit = new WalletAppKit(parameters, file, password);

        try {
            // NOTE change the address of the server if needed (port should stay as it is).
            InetAddress peerAddress = InetAddress.getByName("bujica.zemris.fer.hr");
            this.walletAppKit.setPeerNodes(new PeerAddress(peerAddress, 8080));
        } catch (Exception ignore) {}

        LOGGER.info("Starting to sync blockchain. This might take a few minutes");
        this.walletAppKit.setAutoSave(true);
        this.walletAppKit.startAsync();
        this.walletAppKit.awaitRunning();
        LOGGER.info("Synced blockchain");
    }

    public Wallet getWallet() {
        return this.walletAppKit.wallet();
    }

    public PeerGroup getPeerGroup() {
        return this.walletAppKit.peerGroup();
    }

    @Override
    public void close() {
        walletAppKit.stopAsync();
        walletAppKit.awaitTerminated();
    }
}
