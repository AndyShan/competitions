package sgd;

import java.util.LinkedList;

import org.json.JSONException;

public class ReqAndComThread extends Thread {
	public boolean isEnd = false;
	public LinkedList<String> result;
	public String content;
	public IdObject idObject;
	public Long id1;
	public Long AuId;
	public LinkedList<String> index;

	public ReqAndComThread(String content, Long id1, Long AuId, IdObject idObject, LinkedList<String> result,LinkedList<String> index) {
		this.result = result;
		this.content = content;
		this.idObject = idObject;
		this.id1 = id1;
		this.index = index;
		this.AuId = AuId;
	}

	@Override
	public void run() {
		while (!isEnd) {
			Long[] ids;
			try {
				ids = JsonTools.getRespId(content, "Id");
				if (ids != null&&ids.length!=0) {
					Compute.sort(ids);
					LinkedList<Long> idid = Compute.intersection(idObject.RId, ids);
					if (idid != null && idid.size() != 0) {
						for (Long id : idid) {
							result.add("[" + id1 + "," + id + "," + idObject.Id + "," + AuId + "]");
						}
					}
				}
				index.add("1");
				isEnd = true;
			} catch (JSONException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}
	}
}
