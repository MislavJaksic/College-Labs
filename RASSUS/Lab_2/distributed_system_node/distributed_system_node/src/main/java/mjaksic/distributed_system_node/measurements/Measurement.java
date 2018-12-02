package mjaksic.distributed_system_node.measurements;

import com.opencsv.bean.CsvBindByName;

public class Measurement {

	@CsvBindByName
	private int CO;

	public int getCO() {
		return CO;
	}

	public void setCO(int CO) {
		this.CO = CO;
	}

	@Override
	public String toString() {
		return "Measurement [CO=" + CO + "]";
	}
	

}
