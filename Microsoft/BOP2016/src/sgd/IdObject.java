package sgd;

public class IdObject {
	Long[] RId = null;
	Long[] AuId = null;
	Long[] AfId = null;
	Long[] FId = null;
	Long CId = 0L;
	Long JId = 0L;
	Long Id = 0L;

	public IdObject(int RIdLength, int AuIdLength, int AfIdLength, int FIdLength, Long CId,Long JId,Long Id) {
		RId = new Long[RIdLength];
		AuId = new Long[AuIdLength];
		AfId = new Long[AfIdLength];
		FId = new Long[FIdLength];
		this.CId = CId;
		this.JId = JId;
		this.Id = Id;
	}

	
}
