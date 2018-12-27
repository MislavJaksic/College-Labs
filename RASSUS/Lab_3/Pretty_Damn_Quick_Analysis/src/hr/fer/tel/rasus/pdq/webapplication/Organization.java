/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package hr.fer.tel.rasus.pdq.webapplication;

import com.perfdynamics.pdq.Job;
import com.perfdynamics.pdq.Methods;
import com.perfdynamics.pdq.Node;
import com.perfdynamics.pdq.PDQ;
import com.perfdynamics.pdq.QDiscipline;

/**
 *
 * @author Kreso
 */
public class Organization {

    public static void main(String[] args) {
        PDQ pdq = new PDQ();

        final int m_AP = 1;
        final int m_BP = 10;
        final int m_IM = 1;

        final float p_IM = 0.1f;
        final float p_BP = 0.15f;

        final float S_ZZ = 0.001f;
        final float S_PO = 0.001f;

        final float S_AP = 0.3f;
        final float S_BP = 2.5f / m_BP;
        final float S_IM = 0.5f;

        final float lambda_inc = 0.1f;
        final float lambda_max = 2.0f;

        System.out.print("lambda\t");

        for (int i = 0; i < m_AP; i++) {
            System.out.print("T_AP" + i + "\t");
        }

        for (int i = 0; i < m_BP; i++) {
            System.out.print("T_BP" + i + "\t");
        }

        for (int i = 0; i < m_IM; i++) {
            System.out.print("T_IM" + i + "\t");
        }
        System.out.print("T_ZZ\t");
        System.out.print("T_PO\t");
        System.out.println("T");

        for (float lambda = lambda_inc; lambda < lambda_max + lambda_inc; lambda += lambda_inc) {
            pdq.Init("Web aplikacija");
            pdq.CreateOpen("Zahtjevi", lambda);

            pdq.CreateNode("ZZ", Node.CEN, QDiscipline.FCFS);
            pdq.CreateNode("PO", Node.CEN, QDiscipline.FCFS);

            for (int i = 0; i < m_AP; i++) {
                pdq.CreateNode("AP" + i, Node.CEN, QDiscipline.FCFS);
            }

            for (int i = 0; i < m_BP; i++) {
                pdq.CreateNode("BP" + i, Node.CEN, QDiscipline.FCFS);
            }

            for (int i = 0; i < m_IM; i++) {
                pdq.CreateNode("IM" + i, Node.CEN, QDiscipline.FCFS);
            }

            pdq.SetVisits("ZZ", "Zahtjevi", 1.0f, S_ZZ);
            pdq.SetVisits("PO", "Zahtjevi", 1.0f, S_PO);

            for (int i = 0; i < m_AP; i++) {
                pdq.SetVisits("AP" + i, "Zahtjevi", ((1 - p_IM) / (1 - p_BP)) / m_AP, S_AP);
            }

            for (int i = 0; i < m_BP; i++) {
                pdq.SetVisits("BP" + i, "Zahtjevi", (p_BP * (1 - p_IM) / (1 - p_BP)) / m_BP, S_BP);
            }

            for (int i = 0; i < m_IM; i++) {
                pdq.SetVisits("IM" + i, "Zahtjevi", p_IM / m_IM, S_IM);
            }

            pdq.Solve(Methods.CANON);

            System.out.print(lambda + "\t");

            for (int i = 0; i < m_AP; i++) {
                System.out.print(pdq.GetResidenceTime("AP" + i, "Zahtjevi", Job.TRANS) + "\t");
            }

            for (int i = 0; i < m_BP; i++) {
                System.out.print(pdq.GetResidenceTime("BP" + i, "Zahtjevi", Job.TRANS) + "\t");
            }

            for (int i = 0; i < m_IM; i++) {
                System.out.print(pdq.GetResidenceTime("IM" + i, "Zahtjevi", Job.TRANS) + "\t");
            }

            System.out.print(pdq.GetResidenceTime("ZZ", "Zahtjevi", Job.TRANS) + "\t");

            System.out.print(pdq.GetResidenceTime("PO", "Zahtjevi", Job.TRANS) + "\t");

            System.out.println(pdq.GetResponse(Job.TRANS, "Zahtjevi"));
        }
    }
}
