package mjaksic.distributed_system_node.message;

import java.util.Comparator;
import java.util.List;

public class MessageVectorComparator implements Comparator<Message> {

	@Override
	public int compare(Message message_A, Message message_B) {
		List<Integer> vector_time_A = message_A.vector_time;
		List<Integer> vector_time_B = message_B.vector_time;

		for (int i = 0; i < vector_time_A.size(); i++) {
			if (vector_time_A.get(i) > vector_time_B.get(i)) {
				return 1;
			} else if (vector_time_A.get(i) < vector_time_B.get(i)) {
				return -1;
			}
		}

		return 0;
	}

}
