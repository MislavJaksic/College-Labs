package mjaksic.distributed_system_node.message;

import java.util.Comparator;

public class MessageScalarComparator implements Comparator<Message> {

	@Override
	public int compare(Message message_A, Message message_B) {
		if (message_A.scalar_time == message_B.scalar_time) {
			return 0;
		} else if (message_A.scalar_time > message_B.scalar_time) {
			return 1;
		}
		return -1;
	}

}
