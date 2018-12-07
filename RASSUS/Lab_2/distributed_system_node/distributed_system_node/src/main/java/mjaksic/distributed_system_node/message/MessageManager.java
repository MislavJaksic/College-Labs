package mjaksic.distributed_system_node.message;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MessageManager {
	private static final int destination_port_sentinel = -1;
	
	private Map<Integer, List<Integer>> unconfirmed_messages;
	
	
	
	public MessageManager() {
		this.unconfirmed_messages = new HashMap<Integer, List<Integer>>();
	}
	
	
	
	public synchronized void AddUnconfirmedMessageForPorts(Message message, List<Integer> ports) {
		Message key = this.TransformMessageIntoKey(message);
		List<Integer> value = this.TransformPortsIntoValue(ports);
		
		this.unconfirmed_messages.put(key, value);
		System.out.println("Key=" + key + ", value=" + this.GetUnconfirmedPortsForKey(key));
		
		System.out.println(unconfirmed_messages);
	}
	
	
	
	public synchronized void RecogniseConformationMessage(Message message) {
		int confirmation_port = this.ExtractConfirmationPortFromMessage(message);
		Message normalised_message = this.NormaliseMessage(message);
		Integer key = normalised_message.hashCode();
		
		System.out.println("unconfirmed_messages=" + unconfirmed_messages);
		System.out.println("key=" + key);
		
		List<Integer> current_unconfirmed_ports = this.GetUnconfirmedPortsForKey(key);
		System.out.println("current_unconfirmed_ports=" + current_unconfirmed_ports);
		
		List<Integer> new_unconfimred_ports = this.RemovePortFromPortList(confirmation_port, current_unconfirmed_ports);
		
		if (new_unconfimred_ports.isEmpty()) {
			this.unconfirmed_messages.remove(key);
		} else {
			this.AddUnconfirmedMessageForPorts(message, new_unconfimred_ports);
		}
	}
	
	
	
	private synchronized Message TransformMessageIntoKey(Message message) {
		message.destination_port = MessageManager.destination_port_sentinel;
		
		return message;
	}
	
	private synchronized List<Integer> TransformPortsIntoValue(List<Integer> ports) {
		return ports;
	}
	
	private synchronized int ExtractConfirmationPortFromMessage(Message message) {
		int confirmtion_port = message.destination_port;
		return confirmtion_port;
	}
	
	private synchronized List<Integer> GetUnconfirmedPortsForKey(Integer key) {
		List<Integer> ports = this.unconfirmed_messages.get(key);
		return ports;
	}

	private synchronized List<Integer> RemovePortFromPortList(int port_to_remove, List<Integer> ports) {
		System.out.println("-.-.-.-.-");
		System.out.println("port_to_remove=" + port_to_remove);
		System.out.println("ports=" + ports);
		ArrayList<Integer> new_ports = new ArrayList<Integer>();
		
		for (int port : ports) {
			if (port != port_to_remove) {
				new_ports.add(port);
			}
		}
		
		System.out.println("new_ports" + new_ports);
		System.out.println("-.-.-.-.-");
		return new_ports;
	}
	

	@Override
	public synchronized String toString() {
		return "MessageManager [unconfirmed_messages=" + unconfirmed_messages + "]";
	}

}
