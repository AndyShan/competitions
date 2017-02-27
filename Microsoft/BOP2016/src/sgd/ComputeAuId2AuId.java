package sgd;

import java.util.LinkedHashSet;
import java.util.LinkedList;
import java.util.Map;
import java.util.Set;

public class ComputeAuId2AuId {
	public static LinkedList<String> findHop(Long AuId1, Long AuId2, IdObject[] id1Object, IdObject[] id2Object,
			Map<Long, String> myAA) {
		LinkedList<String> _hop = new LinkedList<String>();
		 _hop.addAll(find2Hop(AuId1, AuId2, id1Object, id2Object));
		_hop.addAll(find2Hop2(AuId1, AuId2, myAA));
		 _hop.addAll(find3Hop(AuId1, AuId2, id1Object, id2Object));
		return _hop;
	}

	/*
	 * find 2-hop 2-hop:[AuId,Id,AuId]
	 */
	public static LinkedList<String> find2Hop(Long AuId1, Long AuId2, IdObject[] id1Object, IdObject[] id2Object) {
		LinkedList<String> _2hop = new LinkedList<String>();
		Set<Long> idSet = new LinkedHashSet<Long>();
		for (IdObject ob : id1Object) {
			int flag = 0;
			if (ob.AuId.length != 0 && ob.AuId != null) {
				for (int i = 0; i < ob.AuId.length; i++) {
					String auid = ob.AuId[i] + "";
					String auid1 = AuId1 + "";
					String auid2 = AuId2 + "";
					if ((auid.contains(auid1) || (auid.contains(auid2))) && flag == 0) {
						flag = 1;
					} else if ((auid.contains(auid1) || (auid.contains(auid2))) && flag == 1) {
						idSet.add(ob.Id);
					}
				}
				flag = 0;
			}
		}

		for (IdObject ob : id2Object) {
			int flag = 0;
			if (ob.AuId.length != 0 && ob.AuId != null) {
				for (int i = 0; i < ob.AuId.length; i++) {
					String auid = ob.AuId[i] + "";
					String auid1 = AuId1 + "";
					String auid2 = AuId2 + "";
					if ((auid.contains(auid1) || (auid.contains(auid2))) && flag == 0) {
						flag = 1;
					} else if ((auid.contains(auid1) || (auid.contains(auid2))) && flag == 1) {
						idSet.add(ob.Id);
					}
					flag = 0;
				}
			}
		}
		if (idSet != null && idSet.size() != 0) {
			for (Long id : idSet) {
				_2hop.add("[" + AuId1 + "," + id + "," + AuId2 + "]");
			}
		}

		return _2hop;
	}

	/*
	 * find 2-hop 2-hop:[AuId,AfId,AuId]
	 */
	public static LinkedList<String> find2Hop2(Long AuId1, Long AuId2, Map<Long, String> myAA) {
		
		LinkedList<String> _2hop = new LinkedList<String>();
		if (myAA.containsKey(AuId1) && myAA.containsKey(AuId2)) {
			String afid1 = myAA.get(AuId1).toString();
			String afid2 = myAA.get(AuId2).toString();
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
					_2hop.add("["+AuId1+","+s+","+AuId2+","+"]");
				}
			}
		}

		return _2hop;
	}

	/*
	 * find 3-hop 3-hop:[AuId,Id,Id,AuId]
	 */
	public static LinkedList<String> find3Hop(Long AuId1, Long AuId2, IdObject[] id1Object, IdObject[] id2Object) {
		LinkedList<String> _3hop = new LinkedList<String>();
		Long[] ids = new Long[id2Object.length];
		for (int i = 0; i < id2Object.length; i++) {
			ids[i] = id2Object[i].Id;
		}
		Compute.sort(ids);
		for (IdObject ob : id1Object) {
			LinkedList<Long> idList = new LinkedList<Long>();
			if (ob.RId != null && ob.RId.length != 0) {
				idList.addAll(Compute.intersection(ob.RId, ids));
			}
			if (idList != null && idList.size() != 0) {
				for (Long l : idList) {
					_3hop.add("[" + AuId1 + "," + ob.Id + "," + l + "," + AuId2 + "]");
				}
			}
		}

		return _3hop;
	}
}
