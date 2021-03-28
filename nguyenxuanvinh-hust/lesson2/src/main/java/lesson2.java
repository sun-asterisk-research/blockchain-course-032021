import org.bitcoinj.core.Base58;
import org.bouncycastle.jce.provider.BouncyCastleProvider;

import java.security.*;
import java.security.interfaces.ECPrivateKey;
import java.security.interfaces.ECPublicKey;
import java.security.spec.ECGenParameterSpec;
import java.security.spec.ECPoint;

public class lesson2 {

    /**
     * used to fix java.security.NoSuchProviderException: no such provider: BC
     */
    static {
        try {
            Security.addProvider(new BouncyCastleProvider());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {

        try{
            KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("EC");
            ECGenParameterSpec ecSpec = new ECGenParameterSpec("secp256k1");
            keyPairGenerator.initialize(ecSpec);
            KeyPair keyPair = keyPairGenerator.generateKeyPair();
            PrivateKey privateKey = keyPair.getPrivate();
            PublicKey publicKey = keyPair.getPublic();
            ECPrivateKey epvt = (ECPrivateKey) privateKey;
            String sepvt = adjustTo64(epvt.getS().toString(16)).toUpperCase();
            System.out.println("Private key: " + sepvt);;

            ECPublicKey epub = (ECPublicKey) publicKey;
            ECPoint pt = epub.getW();
            String sx = adjustTo64(pt.getAffineX().toString(16)).toUpperCase();
            String sy = adjustTo64(pt.getAffineY().toString(16)).toUpperCase();
            String bcPub = "04" + sx + sy;
            System.out.println("Public key: " + bcPub);

            //get Address
            MessageDigest sha = MessageDigest.getInstance("SHA-256");
            byte[] s1 = sha.digest(bcPub.getBytes("UTF-8"));

            MessageDigest rmd = MessageDigest.getInstance("RipeMD160", "BC");
            byte[] r1 = rmd.digest(s1);

            byte[] r2 = new byte[r1.length + 1];
            r2[0] = 0;
            for (int i = 0 ; i < r1.length ; i++) r2[i+1] = r1[i];

            byte[] s2 = sha.digest(r2);
            byte[] s3 = sha.digest(s2);

            byte[] a1 = new byte[100];
            for (int i = 0 ; i < r2.length ; i++) a1[i] = r2[i];
            for (int i = 0 ; i < 5 ; i++) a1[20 + i] = s3[i];

            System.out.println("Address: " + Base58.encode(a1));


        } catch(Exception e){
            e.printStackTrace();
        }
    }

    static private String adjustTo64(String s) {
        switch(s.length()) {
            case 62: return "00" + s;
            case 63: return "0" + s;
            case 64: return s;
            default:
                throw new IllegalArgumentException("not a valid key: " + s);
        }
    }



}
