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
public class Example2 {

    public static void main(String[] args) {
        PDQ pdq = new PDQ();

        final float lambda = 50f;    // Ucestalost dolazaka zahtjeva u rep cekanja lambda = 50 z/s
        final float S = 0.01f;  // Prosjecno vrijeme posluzivanja zahtjeva S = 0.01 s/z

        // Postavljanje pocetnih postavki PDQ sustava
        pdq.Init("Diskovni podsustav");

        // Stvaranje jednog posluzitelja koji obradjuje zahtjeve prema redoslijedu prispjeca
        pdq.CreateNode("Disk", Node.CEN, QDiscipline.FCFS);

        // Stvaranje ulaznog toka zahtjeva
        pdq.CreateOpen("Operacije", lambda);

        // Povezivanje ulaznog toka s posluziteljem i definiranje vremena posluzivanja
        pdq.SetDemand("Disk", "Operacije", S);

        // Pokretanje izracuna
        pdq.Solve(Methods.CANON);

        // Prikaz rezultata
        double T = pdq.GetResidenceTime("Disk", "Operacije", Job.TRANS);
        System.out.printf("Srednje vrijeme cekanja zahtjeva na obradu W = %.02f\n", T - S);

        //Prikaz svih rezultata
        //pdq.Report();
    }
}
