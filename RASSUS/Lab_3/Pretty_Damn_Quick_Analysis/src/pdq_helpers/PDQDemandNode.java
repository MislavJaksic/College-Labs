package pdq_helpers;

public class PDQDemandNode {
	public String node_name = null;
	public String queue_name = null;
	public Float demand = null;
	public Float rho = demand;
	
	
	
	public PDQDemandNode(String node_name, String queue_name, Float demand) {
		this.node_name = node_name;
		this.queue_name = queue_name;
		this.demand = demand;
		this.rho = demand;
	}
	
}
