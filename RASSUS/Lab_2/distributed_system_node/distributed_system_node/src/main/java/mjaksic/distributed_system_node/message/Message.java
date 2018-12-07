package mjaksic.distributed_system_node.message;

import java.io.Serializable;
import java.util.List;

import mjaksic.distributed_system_node.measurement.Measurement;

public class Message implements Serializable {
	private static final long serialVersionUID = 8197605027819193331L;
	
	public Measurement measurement;
	public int scalar_time;
	public List<Integer> vector_time;
	
	public int port_of_origin;
	public int destination_port;

	
	
	public Message(Measurement measurement, int scalar_time, List<Integer> vector_time, int port_of_origin, int destination_port) {
		this.measurement = measurement;
		this.scalar_time = scalar_time;
		this.vector_time = vector_time;
		
		this.port_of_origin = port_of_origin;
		this.destination_port = destination_port;
	}



	@Override
	public String toString() {
		return "Message [" + measurement + ", " + scalar_time + ", " + vector_time
				+ ", " + port_of_origin + ", " + destination_port + "]";
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Message other = (Message) obj;
		if (destination_port != other.destination_port)
			return false;
		if (measurement == null) {
			if (other.measurement != null)
				return false;
		} else if (!measurement.equals(other.measurement))
			return false;
		if (port_of_origin != other.port_of_origin)
			return false;
		if (scalar_time != other.scalar_time)
			return false;
		if (vector_time == null) {
			if (other.vector_time != null)
				return false;
		} else if (!vector_time.equals(other.vector_time))
			return false;
		return true;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + destination_port;
		result = prime * result + ((measurement == null) ? 0 : measurement.hashCode());
		result = prime * result + port_of_origin;
		result = prime * result + scalar_time;
		result = prime * result + ((vector_time == null) ? 0 : vector_time.hashCode());
		return result;
	}
	
}