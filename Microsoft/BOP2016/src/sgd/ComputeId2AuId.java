package sgd;

import java.util.LinkedHashSet;
import java.util.LinkedList;
import java.util.Map;
import java.util.Set;

import org.json.JSONException;

public class ComputeId2AuId {

	public static LinkedList<String> findHop(Long id1, Long AuId, IdObject id1Object, IdObject[] id2Objects,Map<Long,String> myAA)
			throws JSONException {
		LinkedList<String> hop = new LinkedList<String>();
		hop.addAll(find1hop(id1, AuId, id1Object));
		hop.addAll(find2Hop(id1, AuId, id1Object, id2Objects));
		hop.addAll(find3Hop(id1, AuId, id1Object, id2Objects));
		hop.addAll(find3Hop2(id1, AuId, id1Object, id2Objects));
		hop.addAll(find3Hop3(id1, AuId, id1Object, id2Objects));
		hop.addAll(find3Hop4(id1, AuId, id1Object, myAA));
		return hop;
	}

	/*
	 * find:1-hop 1-hop:[Id,AuId]
	 */
	public static LinkedList<String> find1hop(Long id1, Long AuId, IdObject id1Object) {
		System.out.println(1);
		LinkedList<String> _1hop = new LinkedList<String>();
		if (id1Object.AuId != null) {
			for (Long l : id1Object.AuId) {
				String id1AuId = l + "";
				String auId = AuId + "";
				if (auId.contains(id1AuId)) {
					_1hop.add("[" + id1 + "," + AuId + "]");
					break;
				}
			}
		}
		return _1hop;
	}

	/*
	 * find:2-hop 2-hop:[Id,Id,AuId]
	 */
	public static LinkedList<String> find2Hop(Long id1, Long AuId, IdObject id1Object, IdObject[] id2Objects)
			throws JSONException {
		System.out.println(2);
		LinkedList<String> _2hop = new LinkedList<String>();
		Long[] ids = new Long[id2Objects.length];
		for (int i = 0; i < id2Objects.length; i++) {
			ids[i] = id2Objects[i].Id;
		}

		Compute.sort(ids);

		LinkedList<Long> list = Compute.intersection(id1Object.RId, ids);

		if (list != null && list.size() != 0) {
			for (Long id : list) {
				_2hop.add("[" + id1 + "," + id + "," + AuId + "]");
			}
		}

		return _2hop;
	}

	/*
	 * find:3-hop 3-hop:[Id,C.CId,Id,AuId],[Id,J.JId,Id,AuId]
	 */
	public static LinkedList<String> find3Hop(Long id1, Long AuId, IdObject Id1Object, IdObject[] id2Objects) {
		System.out.println(3);
		LinkedList<String> _3hop = new LinkedList<String>();
		if (Id1Object.CId != 0) {
			for (IdObject ob : id2Objects) {
				if (ob.CId != 0 && (ob.CId + "").contains(Id1Object.CId + "")) {
					_3hop.add("[" + id1 + "," + Id1Object.CId + "," + ob.Id + "," + AuId+"]");
				}
			}
		}

		if (Id1Object.JId != 0) {
			for (IdObject ob : id2Objects) {
				if (ob.JId != 0 && (ob.JId + "").contains(Id1Object.JId + "")) {
					_3hop.add("[" + id1 + "," + Id1Object.JId + "," + ob.Id + "," + AuId+"]");
				}
			}
		}

		return _3hop;
	}

	/*
	 * find:3-hop 3-hop:[Id,F.FId,Id,AuId],[Id,AA.AuId,Id,AuId]
	 * 
	 * problem:存在AuId->Id->AuId->Id的成环现象
	 */
	public static LinkedList<String> find3Hop2(Long Id, Long AuId, IdObject id1Object, IdObject[] id2Objects) {
		System.out.println(4);
		LinkedList<String> _3hop = new LinkedList<String>();
		if (id1Object.FId != null && id1Object.FId.length != 0) {
			for (IdObject ob : id2Objects) {
				LinkedList<Long> ids = Compute.intersection(id1Object.FId, ob.FId);
				if (ids != null && ids.size() != 0) {
					for (Long l : ids) {
						_3hop.add("[" + Id + "," + l + "," + ob.Id + "," + AuId + "]");
					}
				}
			}
		}

		if (id1Object.AuId != null && id1Object.AuId.length != 0) {
			for (IdObject ob : id2Objects) {
				LinkedList<Long> ids = Compute.intersection(id1Object.AuId, ob.AuId);
				if (ids != null && ids.size() != 0) {
					for (Long l : ids) {
						_3hop.add("[" + Id + "," + l + "," + ob.Id + "," + AuId + "]");
					}
				}
			}
		}

		return _3hop;
	}

	/*
	 * find:3-hop 3-hop:[Id,Id,Id,AuId]
	 */
	public static LinkedList<String> find3Hop3(Long Id, Long AuId, IdObject id1Object, IdObject[] id2Objects)
			throws JSONException {
		System.out.println(5);
		LinkedList<String> _3hop = new LinkedList<String>();
		if (id2Objects.length < 2) {
			for (IdObject ob : id2Objects) {
				Long[] ids = JsonTools.getRespId("RId="+ob.Id,"Id");
				Compute.sort(ids);
				LinkedList<Long> idid = Compute.intersection(id1Object.RId, ids);
				if (idid!=null&&idid.size()!=0) {
					for (Long id:idid) {
						_3hop.add("["+Id+","+id+","+ob.Id+","+AuId+"]");
					}
				}
			}
		}else {
			/*
			 * 最后的调试——1
			 */
				JsonTools.Id2AuIdByThread(id2Objects,id1Object, Id, AuId, _3hop);
		}

		return _3hop;
	}

	/*
	 * find:3-hop 3-hop:[Id,AuId,AfId,AuId]
	 */
	public static LinkedList<String> find3Hop4(Long Id,Long AuId,IdObject id1Object,Map<Long,String> myAA) {
		System.out.println(6);
		LinkedList<String> _3hop = new LinkedList<String>();
		for (Long id1AuId:id1Object.AuId) {
			if (myAA.containsKey(id1AuId)&&myAA.containsKey(AuId)) {
				String afid1 = id1AuId+"";
				String afid2 = myAA.get(AuId)+"";
				String[] afid1Array = afid1.split(",");
				String[] afid2Array = afid2.split(",");
				Set<String> afidSet = new LinkedHashSet<String>();
				for (int i = 1;i<afid1Array.length;i++) {
					for (int j = 1;j<afid2Array.length;j++) {
						if (afid1Array[i]!=null&&afid2Array[j]!=null&&afid1Array[i].contains(afid2Array[j])) {
							afidSet.add(afid1Array[i]);
						}
					}
				}
				if (afidSet!=null&&afidSet.size()!=0) {
					for (String s : afidSet) {
						_3hop.add("["+Id+","+id1AuId+","+s+","+AuId+"]");
					}
				}
			}
		}
		return _3hop;
	}
}
