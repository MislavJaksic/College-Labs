package experiments;

import pdq_helpers.PDQAnaliser;
import pdq_helpers.PDQDemandNode;

public class Problem2_2 {
	// Service Times
	public static final float S_1 = 0.003f;
	public static final float S_2 = 0.001f;
	public static final float S_3 = 0.01f;
	public static final float S_4 = 0.04f;
	public static final float S_5 = 0.1f;
	public static final float S_6 = 0.13f;
	public static final float S_7 = 0.15f;
	
	// Branch Probabilities
	public static final float p_a = 0.2f;
	public static final float p_b = 0.3f;
	public static final float p_c = 0.5f;
	public static final float p_d = 0.3f;
	public static final float p_e = 0.7f;
	public static final float p_f = 0.6f;
	public static final float p_g = 0.2f;
	public static final float p_h = 0.3f;
	
	// Visits
	public static final float v_1 = 0.0f;
	public static final float v_2 = 0.0f;
	public static final float v_3 = 0.0f;
	public static final float v_4 = 0.0f;
	public static final float v_5 = 0.0f;
	public static final float v_6 = 0.0f;
	public static final float v_7 = 0.0f;

	
	
	public static void main(String[] args) {
		// [Demand] == [rho if system_lambda is 1]
		// An alternative to calculating visits
		float rho_1 = 0.003f;
		float rho_2 = 0.00122f;
		float rho_3 = 0.00376f;
		float rho_4 = 0.01764f;
		float rho_5 = 0.061f;
		float rho_6 = 0.04758f;
		float rho_7 = 0.12795f;
		
		float step = 0.1f;
		float max_lambda = 10.0f;
		
		for (float system_lambda = 0.1f; max_lambda > system_lambda; system_lambda += step) {
			PDQAnaliser analiser = new PDQAnaliser("Problem2_2");
			
			
			PDQDemandNode node_one = new PDQDemandNode("Node_1", "Queue_1", rho_1);
			PDQDemandNode node_two = new PDQDemandNode("Node_2", "Queue_1", rho_2);
			PDQDemandNode node_three = new PDQDemandNode("Node_3", "Queue_1", rho_3);
			PDQDemandNode node_four = new PDQDemandNode("Node_4", "Queue_1", rho_4);
			PDQDemandNode node_five = new PDQDemandNode("Node_5", "Queue_1", rho_5);
			PDQDemandNode node_six = new PDQDemandNode("Node_6", "Queue_1", rho_6);
			PDQDemandNode node_seven = new PDQDemandNode("Node_7", "Queue_1", rho_7);
			
			

			analiser.CreateOpen("Queue_1", system_lambda);
			
			analiser.AddPDQNode(node_one);
			analiser.AddPDQNode(node_two);
			analiser.AddPDQNode(node_three);
			analiser.AddPDQNode(node_four);
			analiser.AddPDQNode(node_five);
			analiser.AddPDQNode(node_six);
			analiser.AddPDQNode(node_seven);
			
			analiser.Solve();
			
			
			
			double T = analiser.GetResponse("Queue_1");
			
			System.out.print("(");
			System.out.printf("%.1f", system_lambda);
			System.out.print(",");
			System.out.printf("%.3f", T);
			System.out.print(")");
			System.out.println();
			
	        
	        //analiser.PrintReport();
		}
		
	}
	
}
