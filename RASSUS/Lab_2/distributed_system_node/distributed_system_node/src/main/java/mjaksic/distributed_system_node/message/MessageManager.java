package mjaksic.distributed_system_node.message;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class MessageManager {
	private static final int destination_sentinel = -1;

	private Set<Message> message_without_response;

	private Set<Message> measurement_messages;

	
	
	public MessageManager() {
		this.message_without_response = new HashSet<Message>();
		this.measurement_messages = new HashSet<Message>();
	}

	
	
	public synchronized void PutMessageWithoutResponse(Message message) {
		this.message_without_response.add(message);
	}

	public synchronized void RegisterResponse(Message message) {
		this.message_without_response.remove(message);
	}

	public synchronized Set<Message> GetUnconfirmedMessages() {
		Set<Message> messages = new HashSet<>(this.message_without_response);
		return messages;
	}

	

	public synchronized void PutMeasurementMessage(Message measurement) {
		Message clone_measurement = new Message(measurement);
		clone_measurement.destination_port = MessageManager.destination_sentinel;

		this.measurement_messages.add(clone_measurement);
	}
	
	

	public synchronized List<Message> GetScalarSortedMeasurementMessages() {
		ArrayList<Message> array = new ArrayList<Message>();
		for (Message message : this.measurement_messages) {
			array.add(message);
		}

		MessageScalarComparator comparator = new MessageScalarComparator();
		array.sort(comparator);

		return array;
	}

	public synchronized List<Message> GetVectorSortedMeasurementMessages() {
		ArrayList<Message> array = new ArrayList<Message>();
		for (Message message : this.measurement_messages) {
			array.add(message);
		}

		MessageVectorComparator comparator = new MessageVectorComparator();
		array.sort(comparator);

		return array;
	}

	
	
	public synchronized double GetAverageMeasurement() {
		ArrayList<Message> measurements = new ArrayList<Message>();
		for (Message message : this.measurement_messages) {
			measurements.add(message);
		}

		double sum = 0.0;
		for (Message message : measurements) {
			sum += message.measurement.getCO();
		}

		return sum / measurements.size();
	}

	
	
	public synchronized void DeleteMeasurementMessages() {
		this.measurement_messages = new HashSet<Message>();
	}

	
	
	@Override
	public synchronized String toString() {
		return "MessageManager [message_without_response=" + message_without_response + "]";
	}

}
