package mjaksic.distributed_system_node.measurement;

import java.io.Serializable;

import com.opencsv.bean.CsvBindByName;

public class Measurement implements Serializable {
	private static final long serialVersionUID = -4961340919562810234L;
	
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
