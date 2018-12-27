package solution;

import com.perfdynamics.pdq.Job;
import com.perfdynamics.pdq.Methods;
import com.perfdynamics.pdq.Node;
import com.perfdynamics.pdq.PDQ;
import com.perfdynamics.pdq.QDiscipline;

public class Problem234 {
	// Pretty Damn Quick Analiser Constants
	public static final int node_type = Node.CEN;
	public static final int service_discipline = QDiscipline.FCFS; // First Come First Serve, like FIFO
	public static final int workload_stream = Job.TRANS; // for open queueing
	public static final int solution_method = Methods.CANON; // for open queueing
	
	public static final int m = Methods.CANON; // for open queueing
	
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
	
	public static final PDQ analiser = new PDQ();
	
	public static void main(String[] args) {
		
	}
	
	/**
	 * 
	 * @param system_name A system under analysis.
	 */
	private static void Initialise(String system_name) {
		Problem234.analiser.Init(system_name);
	}
	
	/**
	 * 
	 * @param node_name Descriptive node name.
	 */
	private static void CreateNode(String node_name) {
		Problem234.analiser.CreateNode(node_name, Problem234.node_type , Problem234.service_discipline);
	}

	/**
	 * 
	 * @param queue_name
	 * @param lambda
	 */
	private static void CreateOpen(String queue_name, float lambda) {
		Problem234.analiser.CreateOpen(queue_name, lambda);
	}

	private static void SetDemand(String node_name, String queue_name, float service_time) {
		Problem234.analiser.SetDemand(node_name, queue_name, service_time);
	}
	
	private static void SetVisits(String node_name, String queue_name, float visits, float service_time) {
		Problem234.analiser.SetVisits(node_name, queue_name, visits, service_time);
	}
	
	private static void Solve() {
		Problem234.analiser.Solve(Problem234.solution_method);
	}
	
	/**
	 * 
	 * @param node_name
	 * @param queue_name
	 * @return RHO_N, N=1..max_node,  
	 */
	private static double GetUtilization(String node_name, String queue_name) {
		return Problem234.analiser.GetUtilization(node_name, queue_name, Problem234.workload_stream);
	}
	
	/**
	 * 
	 * @param node_name
	 * @param queue_name
	 * @return T_N, N = 1..max_node, node retention time
	 */
	private static double GetResidenceTime(String node_name, String queue_name) {
		return Problem234.analiser.GetResidenceTime(node_name, queue_name, Problem234.workload_stream);
	}
	
	/**
	 * 
	 * @param queue_name
	 * @return T, total system retention time
	 */
	private static double GetResponse(String queue_name) {
		return Problem234.analiser.GetResponse(Problem234.workload_stream, queue_name);
	}
	
	/**
	 * 
	 * @param node_name
	 * @param queue_name
	 * @return N_N, N=1..max_node, node request retention
	 */
	private static double GetQueueLength(String node_name, String queue_name) {
		return Problem234.analiser.GetQueueLength(node_name, queue_name, Problem234.workload_stream);
	}
	
	private static void PrintReport() {
		Problem234.analiser.Report();
	}

}
