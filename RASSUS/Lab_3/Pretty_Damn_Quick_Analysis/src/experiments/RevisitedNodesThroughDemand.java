package experiments;

import pdq_helpers.PDQAnaliser;
import pdq_helpers.PDQDemandNode;

public class RevisitedNodesThroughDemand {

	public static void main(String[] args) {
		PDQAnaliser analiser = new PDQAnaliser("SimpleWebSystem");
		
		float system_lambda = 1.00f;
		
		float rho_1 = 0.333f;
		PDQDemandNode node_one = new PDQDemandNode("Node_1", "Queue_1", rho_1);
		
		float rho_2 = 0.116f;
		PDQDemandNode node_two = new PDQDemandNode("Node_2", "Queue_1", rho_2);
		
		
		
		analiser.CreateOpen("Queue_1", system_lambda);
		
		analiser.AddPDQNode(node_one);
		analiser.AddPDQNode(node_two);
		
		analiser.Solve();
        
        analiser.PrintReport();
	}

}
