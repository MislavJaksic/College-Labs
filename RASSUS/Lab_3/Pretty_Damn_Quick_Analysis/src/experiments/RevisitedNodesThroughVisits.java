package experiments;

import pdq_helpers.PDQAnaliser;
import pdq_helpers.PDQVisitsServiceNode;

public class RevisitedNodesThroughVisits {

	public static void main(String[] args) {
		PDQAnaliser analiser = new PDQAnaliser("SimpleWebSystem");
		
		float system_lambda = 1.00f;
		
		float visits_1 = 3.33f;
		float service_time_1 = 0.1f;
		PDQVisitsServiceNode node_one = new PDQVisitsServiceNode("Node_1", "Queue_1", visits_1, service_time_1);
		
		float visits_2 = 2.33f;
		float service_time_2 = 0.05f;
		PDQVisitsServiceNode node_two = new PDQVisitsServiceNode("Node_2", "Queue_1", visits_2, service_time_2);
		
		
		
		analiser.CreateOpen("Queue_1", system_lambda);
		
		analiser.AddPDQNode(node_one);
		analiser.AddPDQNode(node_two);
		
		analiser.Solve();
        
        analiser.PrintReport();
	}

}
