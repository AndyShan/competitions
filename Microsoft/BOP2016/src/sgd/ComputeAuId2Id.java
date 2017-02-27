package sgd;

import java.util.LinkedHashSet;
import java.util.LinkedList;
import java.util.Map;
import java.util.Set;

import org.json.JSONException;

public class ComputeAuId2Id {
	public static LinkedList<String> findHop(Long AuId, Long id2, IdObject[] id1Objects, IdObject id2Object,Map<Long,String> myAA)
			throws JSONException {
		LinkedList<String> hop = new LinkedList<String>();
		hop.addAll(find1hop(AuId, id2, id2Object));
		hop.addAll(find2Hop(AuId,id2,id1Objects,id2Object));
		hop.addAll(find3Hop(AuId, id2, id1Objects, id2Object));
		hop.addAll(find3Hop2(AuId, id2, id1Objects, id2Object));
		hop.addAll(find3Hop3(AuId, id2, id1Objects, id2Object));
		hop.addAll(find3Hop4(AuId, id2, id1Objects, id2Object,myAA));
		return hop;
	}

	/*
	 * find:1-hop
	 * 1-hop:[AuId,Id]
	 */
	public static LinkedList<String> find1hop(Long AuId, Long id2, IdObject id2Object) {
		System.out.println(1);
		LinkedList<String> _1hop = new LinkedList<String>();
		if (id2Object.AuId!=null) {
			for (Long l:id2Object.AuId) {
				String id2AuId = l+"";
				String auId = AuId+"";
				if (auId.contains(id2AuId)) {
					_1hop.add("["+AuId+","+id2+"]");
					break;
				}
			}
		}
		return _1hop;
	}
	
	/*
	 * find:2-hop
	 * 2-hop:[AuId,Id,Id]
	 */
	public static LinkedList<String> find2Hop(Long AuId,Long id2,IdObject[] id1Objects ,IdObject id2Object) throws JSONException {
		System.out.println(2);
		LinkedList<String> _2hop = new LinkedList<String>();
		for (IdObject i :id1Objects) {
			if (i.RId!=null&&i.RId.length!=0) {
				for (Long rid:i.RId) {
					String idid = rid+"";
					String idid2 = id2+"";
					if (idid.contains(idid2)) {
						_2hop.add("["+AuId+","+i.Id+","+id2+"]");
					}
				}
			}
		}
		
		return _2hop;
	}
	
	/*
	 * find:3-hop
	 * 3-hop:[AuId,Id,C.CId,Id],[AuId,Id,J.JId,Id]
	 */
	public static LinkedList<String> find3Hop(Long AuId,Long id2,IdObject[] Id1Objects,IdObject id2Object) {
		System.out.println(3);
		LinkedList<String> _3hop = new LinkedList<String>();
		for (IdObject ob:Id1Objects) {
			String cidid = ob.CId+"";
			String cidid2 = id2Object.CId+"";
			String jidid = ob.JId+"";
			String jidid2 = id2Object.JId+"";
			if (ob.CId!=0&&id2Object.CId!=0&&cidid.contains(cidid2)) {
				_3hop.add("["+AuId+","+ob.Id+","+ob.CId+","+id2+"]");
			}
			
			if (ob.JId!=0&&id2Object.JId!=0&&jidid.contains(jidid2)) {
				_3hop.add("["+AuId+","+ob.Id+","+ob.JId+","+id2+"]");
			}
		}
		return _3hop;
	}
	
	/*
	 * find:3-hop
	 * 3-hop:[AuId,Id,F.FId,Id],[AuId,Id,AA.AuId,Id]
	 * 
	 * problem:存在AuId->Id->AuId->Id的成环现象
	 */
	public static LinkedList<String> find3Hop2(Long AuId,Long id2,IdObject[] id1Objects,IdObject id2Object) {
		System.out.println(4);
		LinkedList<String> _3hop = new LinkedList<String>();
		for (IdObject ob:id1Objects) {
			if (ob.FId!=null&&id2Object.FId!=null&&ob.FId.length!=0&&id2Object.FId.length!=0) {
				LinkedList<Long> fids = Compute.intersection(ob.FId, id2Object.FId);
				if (fids != null&&fids.size()!=0) {
					for (Long l:fids) {
						_3hop.add("["+AuId+","+ob.Id+","+l+","+id2+"]");
					}
				}
			}
		}
		
		for (IdObject ob:id1Objects) {
			if (ob.AuId!=null&&id2Object.AuId!=null&&ob.AuId.length!=0&&id2Object.AuId.length!=0) {
				LinkedList<Long> auids = Compute.intersection(ob.AuId, id2Object.AuId);
				if (auids != null&&auids.size()!=0) {
					for (Long l:auids) {
						_3hop.add("["+AuId+","+ob.Id+","+l+","+id2+"]");
					}
				}
			}
		}
		return _3hop;
	}
	
	/*
	 * find:3-hop
	 * 3-hop:[AuId,Id,Id,Id]
	 */
	public static LinkedList<String> find3Hop3(Long AuId,Long id2,IdObject[] id1Objects,IdObject id2Object) throws JSONException {
		System.out.println(5);
		LinkedList<String> _3hop = new LinkedList<String>();
		Long[] id3 = JsonTools.getRespId("RId="+id2, "Id");
		Compute.sort(id3);
		for (IdObject ob:id1Objects) {
			if (ob.RId!=null&&ob.RId.length!=0) {
				LinkedList<Long> result = Compute.intersection(ob.RId, id3);
				for (Long l:result) {
					_3hop.add("["+AuId+","+ob.Id+","+l+","+id2+"]");
				}
			}
		}
		
		return _3hop;
	}
	
	/*
	 * find:3-hop
	 * 3-hop:[AuId,AfId,AuId,Id]
	 */
	public static LinkedList<String> find3Hop4(Long AuId,Long id2,IdObject[] id1Objects,IdObject id2Object,Map<Long,String> myAA) throws JSONException {
		System.out.println(6);
		LinkedList<String> _3hop = new LinkedList<String>();
		for (Long id2AuId : id2Object.AuId) {
			if (myAA.containsKey(AuId)&&myAA.containsKey(id2AuId)) {
				String afid1 = myAA.get(AuId);
				String afid2 = myAA.get(id2AuId);
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
						_3hop.add("["+AuId+","+id2AuId+","+s+","+id2+"]");
					}
				}
				
			}
		}
		return _3hop;
	}
}
