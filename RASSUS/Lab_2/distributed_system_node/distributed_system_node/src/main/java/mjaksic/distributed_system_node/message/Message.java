package mjaksic.distributed_system_node.message;

import java.io.Serializable;
import java.util.List;

import mjaksic.distributed_system_node.measurement.Measurement;

public class Message implements Serializable {
	
	private static final long serialVersionUID = -8267139628691987323L;
	
	public Measurement measurement;
	public int scalar_value;
	public List<Integer> vector_value;
	
	public boolean is_confirm;

	
	
	public Message(Measurement measurement, int scalar_value, List<Integer> vector_value, boolean is_confirm) {
		this.measurement = measurement;
		this.scalar_value = scalar_value;
		this.vector_value = vector_value;
		
		this.is_confirm = is_confirm;
	}
}