/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package hr.fer.tel.rassus.pdq.examples;

import com.perfdynamics.pdq.Job;
import com.perfdynamics.pdq.Methods;
import com.perfdynamics.pdq.Node;
import com.perfdynamics.pdq.PDQ;
import com.perfdynamics.pdq.QDiscipline;

/**
 *
 * @author Kreso
 */
public class Example3 {

    public static void main(String[] args) {
        PDQ pdq = new PDQ();

        final float lambda = 125f;    // Ucestalost dolazaka zahtjeva u rep cekanja lambda = 125 p/s
        final float S = 0.002f;  // Prosjecno vrijeme posluzivanja zahtjeva S = 0.002 s/p

        // Postavljanje pocetnih postavki PDQ sustava
        pdq.Init("Mrezni podsustav");

        // Stvaranje jednog posluzitelja koji obradjuje zahtjeve prema redoslijedu prispjeca
        pdq.CreateNode("Posluzitelj", Node.CEN, QDiscipline.FCFS);

        // Stvaranje ulaznog toka zahtjeva
        pdq.CreateOpen("Paketi", lambda);

        // Povezivanje ulaznog toka s posluziteljem i definiranje vremena posluzivanja
        pdq.SetDemand("Posluzitelj", "Paketi", S);

        // Pokretanje izracuna
        pdq.Solve(Methods.CANON);

        // Prikaz rezultata
        double rho = pdq.GetUtilization("Posluzitelj", "Paketi", Job.TRANS);
        System.out.printf("Prosječna zaposlenost posluzitelja rho = %.02f\n", rho);

        double T = pdq.GetResidenceTime("Posluzitelj", "Paketi", Job.TRANS);
        System.out.printf("Srednje vrijeme zadrzavanja paketa T = %.06f\n", T);

        double N = pdq.GetQueueLength("Posluzitelj", "Paketi", Job.TRANS);
        System.out.printf("Srednji broj paketa u repu N = %.02f\n", N);

        //Prikaze svih rezultata
        //pdq.Report();
    }
}
