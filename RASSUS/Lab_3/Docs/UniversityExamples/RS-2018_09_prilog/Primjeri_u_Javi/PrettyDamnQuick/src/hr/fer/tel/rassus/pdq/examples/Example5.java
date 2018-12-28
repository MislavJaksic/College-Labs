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
public class Example5 {

    public static void main(String[] args) {
        PDQ pdq = new PDQ();

        final float lambda = 0.1f; // Ucestalost dolazaka zahtjeva u rep cekanja lambda = 0.1 z/s
        final float S1 = 1.0f; // Prosjecno vrijeme posluzivanja zahtjeva S1 = 1.0 s/z
        final float S2 = 2.0f; // Prosjecno vrijeme posluzivanja zahtjeva S2 = 2.0 s/z
        final float S3 = 3.0f; // Prosjecno vrijeme posluzivanja zahtjeva S3 = 3.0 s/z

        // Postavljanje pocetnih postavki PDQ sustava
        pdq.Init("Serija tri posluzitelja");

        // Stvaranje ulaznog toka zahtjeva
        pdq.CreateOpen("Zahtjevi", lambda);

        // Stvaranje tri posluzitelja koji zahtjeve posluzuju prema redoslijedu prispjeca
        pdq.CreateNode("Posluzitelj1", Node.CEN, QDiscipline.FCFS);
        pdq.CreateNode("Posluzitelj2", Node.CEN, QDiscipline.FCFS);
        pdq.CreateNode("Posluzitelj3", Node.CEN, QDiscipline.FCFS);

        // Povezivanje ulaznog toka s posluziteljima
        pdq.SetDemand("Posluzitelj1", "Zahtjevi", S1);
        pdq.SetDemand("Posluzitelj2", "Zahtjevi", S2);
        pdq.SetDemand("Posluzitelj3", "Zahtjevi", S3);

        // Pokretanje izracuna
        pdq.Solve(Methods.CANON);

        // Prikaz rezultata
        double T1 = pdq.GetResidenceTime("Posluzitelj1", "Zahtjevi", Job.TRANS);
        double T2 = pdq.GetResidenceTime("Posluzitelj2", "Zahtjevi", Job.TRANS);
        double T3 = pdq.GetResidenceTime("Posluzitelj3", "Zahtjevi", Job.TRANS);
        System.out.printf("Srednja vremena zadržavanja T1 = %.06f, T2 = %.06f, T3 = %.06f\n", T1, T2, T3);

        double T = pdq.GetResponse(Job.TRANS, "Zahtjevi");
        System.out.printf("Srednje vrijeme zadržavanja u sustavu T = %.06f\n", T);

        double N1 = pdq.GetQueueLength("Posluzitelj1", "Zahtjevi", Job.TRANS);
        double N2 = pdq.GetQueueLength("Posluzitelj2", "Zahtjevi", Job.TRANS);
        double N3 = pdq.GetQueueLength("Posluzitelj3", "Zahtjevi", Job.TRANS);
        System.out.printf("Srednji broj zahtjeva u repu N1 = %.02f, N2 = %.02f, N3 = %.02f\n", N1, N2, N3);
        System.out.printf("Srednji broj zahtjeva u sustavu N = %.06f\n", N1 + N2 + N3);

        //Prikaze svih rezultata
        //pdq.Report();
    }
}
