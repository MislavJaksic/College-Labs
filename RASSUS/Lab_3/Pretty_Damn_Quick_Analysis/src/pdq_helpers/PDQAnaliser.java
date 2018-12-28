package pdq_helpers;

import com.perfdynamics.pdq.PDQ;
import com.perfdynamics.pdq.Job;
import com.perfdynamics.pdq.Methods;
import com.perfdynamics.pdq.Node;
import com.perfdynamics.pdq.QDiscipline;



public class PDQAnaliser {
	// Pretty Damn Quick Analiser Constants
	public static final int node_type = Node.CEN;
	public static final int service_discipline = QDiscipline.FCFS; // First Come First Serve, like FIFO
	public static final int workload_stream = Job.TRANS; // for open queueing
	public static final int solution_method = Methods.CANON; // for open queueing
	
	PDQ analiser = new PDQ();
	

	
	public PDQAnaliser(String system_name) {
		this.Initialise(system_name);
	}

	
	
	/**
	 * 
	 * @param system_name A system under analysis.
	 */
	private void Initialise(String system_name) {
		this.analiser.Init(system_name);
	}
	
	
	/**
	 * 
	 * @param node
	 */
	public void AddPDQNode(PDQVisitsServiceNode node) {
		this.CreateNode(node.node_name);
		
		this.SetVisits(node.node_name, node.queue_name, node.visits, node.service_time);
	}
	
	/**
	 * 
	 * @param node
	 */
	public void AddPDQNode(PDQDemandNode node) {
		this.CreateNode(node.node_name);
		
		this.SetDemand(node.node_name, node.queue_name, node.demand);
	}
	
	
	
	/**
	 * 
	 * @param node_name Descriptive node name.
	 */
	public void CreateNode(String node_name) {
		this.analiser.CreateNode(node_name, PDQAnaliser.node_type, PDQAnaliser.service_discipline);
	}

	/**
	 * 
	 * @param workload_name
	 * @param system_lambda System global lambda, the intensity of incoming requests
	 */
	public void CreateOpen(String workload_name, float system_lambda) {
		this.analiser.CreateOpen(workload_name, system_lambda);
	}

	/**
	 * 
	 * @param node_name
	 * @param queue_name
	 * @param demand Calculated as demand = rho_N = service_time_N * lambda_N
	 */
	public void SetDemand(String node_name, String queue_name, float demand) {
		this.analiser.SetDemand(node_name, queue_name, demand);
	}
	
	/**
	 * 
	 * @param node_name
	 * @param queue_name
	 * @param visits Number of visits based on probability of error
	 * @param service_time S_N
	 */
	public void SetVisits(String node_name, String queue_name, float visits, float service_time) {
		this.analiser.SetVisits(node_name, queue_name, visits, service_time);
	}
	
	
	
	public void Solve() {
		this.analiser.Solve(PDQAnaliser.solution_method);
	}
	
	
	
	public void PrintReport() {
		this.analiser.Report();
	}
	
	/**
	 * If defining nodes with visits-service_time -> rho_N
	 * @param node_name
	 * @param queue_name
	 * @return rho_N, N=1..max_node 
	 */
	public double GetUtilization(String node_name, String queue_name) {
		return this.analiser.GetUtilization(node_name, queue_name, PDQAnaliser.workload_stream);
	}
	
	/**
	 * 
	 * @param node_name
	 * @param queue_name
	 * @return N_N, N=1..max_node, number of requests in node queue
	 */
	public double GetQueueLength(String node_name, String queue_name) {
		return this.analiser.GetQueueLength(node_name, queue_name, PDQAnaliser.workload_stream);
	}
	
	/**
	 * 
	 * @param node_name
	 * @param queue_name
	 * @return T_N * visits_N, N = 1..max_node, node retention time
	 */
	public double GetResidenceTime(String node_name, String queue_name) {
		return this.analiser.GetResidenceTime(node_name, queue_name, PDQAnaliser.workload_stream);
	}
	
	/**
	 * 
	 * @param queue_name
	 * @return T, total system retention time
	 */
	public double GetResponse(String queue_name) {
		return this.analiser.GetResponse(PDQAnaliser.workload_stream, queue_name);
	}

}
