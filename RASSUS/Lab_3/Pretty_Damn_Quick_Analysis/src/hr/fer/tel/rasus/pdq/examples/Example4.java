/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package hr.fer.tel.rasus.pdq.examples;

import com.perfdynamics.pdq.Job;
import com.perfdynamics.pdq.Methods;
import com.perfdynamics.pdq.Node;
import com.perfdynamics.pdq.PDQ;
import com.perfdynamics.pdq.QDiscipline;

/**
 *
 * @author Kreso
 */
public class Example4 {

    public static void main(String[] args) {
        PDQ pdq = new PDQ();

        final float lambda = 0.5f; // Ucestalost dolazaka zahtjeva u rep cekanja lambda = 0.5 z/s
        final float S = 1.0f; // Prosjecno vrijeme posluzivanja zahtjeva S = 1.0 s/z

        // Postavljanje pocetnih postavki PDQ sustava
        pdq.Init("Posluzitelj s repom");

        // Stvaranje jednog posluzitelja koji obradjuje zahtjeve prema redoslijedu prispjeca
        pdq.CreateNode("Posluzitelj", Node.CEN, QDiscipline.FCFS);

        // Stvaranje ulaznog toka zahtjeva
        pdq.CreateOpen("Zahtjevi", lambda);

        // Povezivanje ulaznog toka s posluziteljem i definiranje vremena posluzivanja
        pdq.SetDemand("Posluzitelj", "Zahtjevi", S);

        // Pokretanje izracuna
        pdq.Solve(Methods.CANON);

        // Prikaz rezultata
        double rho = pdq.GetUtilization("Posluzitelj", "Zahtjevi", Job.TRANS);
        System.out.printf("Prosječna zaposlenost rho = %.02f\n", rho);

        double T = pdq.GetResidenceTime("Posluzitelj", "Zahtjevi", Job.TRANS);
        System.out.printf("Srednje vrijeme zadržavanja T = %.06f\n", T);

        double N = pdq.GetQueueLength("Posluzitelj", "Zahtjevi", Job.TRANS);
        System.out.printf("Srednji broj zahtjeva u repu N = %.02f\n", N);

        //Prikaze svih rezultata
        //pdq.Report();
    }
}
