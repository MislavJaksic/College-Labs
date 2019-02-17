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
		return "[CO=" + CO + "]";
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + CO;
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Measurement other = (Measurement) obj;
		if (CO != other.CO)
			return false;
		return true;
	}

}
