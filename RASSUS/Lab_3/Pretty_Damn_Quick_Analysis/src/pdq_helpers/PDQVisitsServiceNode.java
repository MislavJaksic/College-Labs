package pdq_helpers;

public class PDQVisitsServiceNode {
	public String node_name = null;
	public String queue_name = null;
	public Float visits = null;
	public Float service_time = null;
	
	
	
	public PDQVisitsServiceNode(String node_name, String queue_name, Float visits, Float service_time) {
		this.node_name = node_name;
		this.queue_name = queue_name;
		this.visits = visits;
		this.service_time = service_time;
	}

	@Override
	public String toString() {
		return "PDQVisitsServiceNode [node_name=" + node_name + ", queue_name=" + queue_name + ", visits="
				+ visits + ", service_time=" + service_time + "]";
	}
	
}
