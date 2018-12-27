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
public class Example6b {

    public static void main(String[] args) {
        PDQ pdq = new PDQ();

        final float lambda = 3f; // Ucestalost dolazaka zahtjeva u rep cekanja lambda = 3 upit/min
        final float S = 2f; // Prosjecno vrijeme posluzivanja zahtjeva S = 2 min/upit

        // Pomocne varijable za odredivanje imena cvorova i repova u PDQ mrezi
        String nName;
        String cName;

        int m = 18; // Broj paralelnih posluzitelja s privatnim repom

        // Postavljanje pocetnih postavki PDQ sustava
        pdq.Init("Aplikacija korisnicke podrske");
        pdq.SetTUnit("Min"); //minuta kao vremenska jedinica

        // Za svaki posluzitelj izgradi cvor i rep cekanja
        for (int i = 0; i < m; i++) {
            nName = "Serv " + i;
            cName = "Clnt " + i;

            // Stvaranje jednog posluzitelja koji zahtjeve obradjuje prema redoslijedu prispjeca
            pdq.CreateNode(nName, Node.CEN, QDiscipline.FCFS);

            // Stvaranje ulaznog toka zadataka za svaki rep cekanja
            // U svaki od "m" repova cekanja dolazi "lambda/m" zahtjeva/min
            pdq.CreateOpen(cName, lambda / m);
        }

        // Povezi repove cekanja s posluziteljima i definiraj vrijeme posluzivanja
        for (int i = 0; i < m; i++) {

            nName = "Serv " + i;
            cName = "Clnt " + i;

            pdq.SetDemand(nName, cName, S);
        }

        // Pokretanje izracuna
        pdq.Solve(Methods.CANON);

        //Prikaz rezultata
        double T = pdq.GetResponse(Job.TRANS, "Clnt 1");
        System.out.printf("Srednje vrijeme cekanja klijenta na obradu W =  %.06f\n", T - S);

        // Prikaz svih rezultata
        //pdq.Report();
    }
}
  
  