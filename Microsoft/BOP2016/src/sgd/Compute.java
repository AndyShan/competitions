package sgd;

import java.util.LinkedList;
import java.util.Queue;

import org.json.JSONException;

public class Compute {

	public static LinkedList<String> findHop(Long id1, Long id2, IdObject id1Object, IdObject id2Object)
			throws JSONException {
		LinkedList<String> hop = new LinkedList<String>();
		hop.addAll(find1Hop(id1, id2, id1Object, id2Object));
		hop.addAll(find2Hop_1(id1, id2, id1Object, id2Object));
		hop.addAll(find2Hop_2(id1, id2, id1Object, id2Object));
		hop.addAll(find2Hop_3(id1, id2, id1Object, id2Object));
		hop.addAll(find3Hop(id1, id2, id1Object, id2Object));
		hop.addAll(find3Hop2(id1, id2, id1Object, id2Object));
		hop.addAll(find3Hop3(id1, id2, id1Object, id2Object));
		hop.addAll(find3Hop4(id1, id2, id1Object, id2Object));
		return hop;
	}

	/*
	 * 查找1-hop结果 1-hop:[Id,Id]
	 */
	public static LinkedList<String> find1Hop(Long id1, Long id2, IdObject id1Object, IdObject id2Object) {
		System.out.println(1);
		LinkedList<String> _1Hop = new LinkedList<String>();
		for (Long RId : id1Object.RId) {
			String rid = RId+"";
			String idid2 = id2+"";
			if (rid.contains(idid2)) {
				_1Hop.add("[" + id1 + "," + id2 + "]");
				break;
			}
		}
		return _1Hop;
	}

	/*
	 * 查找2-hop结果 2-hop:[Id,C.CId,Id],[Id,J.JId,Id]
	 */
	public static LinkedList<String> find2Hop_1(Long id1, Long id2, IdObject id1Object, IdObject id2Object) {
		System.out.println(2);
		LinkedList<String> _2Hop = new LinkedList<String>();
		if (id1Object.CId != null && id2Object.CId != null && id1Object.CId != 0 && id2Object.CId != 0) {
			String cid1 = id1Object.CId + "";
			String cid2 = id2Object.CId + "";
			if (cid1.contains(cid2)) {
				_2Hop.add("[" + id1 + "," + id1Object.CId + "," + id2 + "]");
			}

		}
		if (id1Object.JId != null && id2Object.JId != null && id1Object.JId != 0 && id2Object.JId != 0
				&& id1Object.JId == id2Object.JId) {
			String jid1 = id1Object.JId + "";
			String jid2 = id2Object.JId + "";
			if (jid1.contains(jid2)) {
				_2Hop.add("[" + id1 + "," + id1Object.JId + "," + id2 + "]");
			}
			_2Hop.add("[" + id1 + "," + id1Object.JId + "," + id2 + "]");
		}
		return _2Hop;
	}

	/*
	 * 查找2-hop结果 2-hop:[Id,F.FId,Id],[Id,AA.AuId,Id]
	 */
	public static LinkedList<String> find2Hop_2(Long id1, Long id2, IdObject id1Object, IdObject id2Object) {
		System.out.println(3);
		LinkedList<String> _2Hop = new LinkedList<String>();
		if (id1Object.FId != null && id2Object.FId != null) {
			LinkedList<Long> fid = intersection(id1Object.FId, id2Object.FId);
			if (fid != null) {
				for (Long f : fid) {
					_2Hop.add("[" + id1 + "," + f + "," + id2 + "]");
				}
			}
		}
		if (id1Object.AuId != null && id2Object.AuId != null) {
			LinkedList<Long> auid = intersection(id1Object.AuId, id2Object.AuId);
			if (auid != null) {
				for (Long au : auid) {
					_2Hop.add("[" + id1 + "," + au + "," + id2 + "]");
				}
			}
		}
		return _2Hop;
	}

	/*
	 * 查找2-hop结果 2-hop:[Id,Id,Id]
	 */
	public static LinkedList<String> find2Hop_3(Long id1, Long id2, IdObject id1Object, IdObject id2Object)
			throws JSONException {
		System.out.println(4);
		LinkedList<String> _2Hop = new LinkedList<String>();
		if (id1Object.RId != null && id1Object.RId.length != 0) {
			IdObject[] idObjects = JsonTools.getUnionResp(idUnion("Id", id1Object.RId));
			if (idObjects != null) {
				for (IdObject ob : idObjects) {
					if (ob.RId != null) {
						for (int i = 0; i < ob.RId.length; i++) {
							String ob_RId = ob.RId[i] + "";
							String id2_s = id2 + "";
							if (ob_RId.contains(id2_s)) {
								_2Hop.add("[" + id1 + "," + ob.Id + "," + id2 + "]");
							}
						}

					}

				}
			}

		}
		return _2Hop;
	}

	/*
	 * 查找3-hop结果 3-hop:[Id,CId,Id,Id],[Id,JId,Id,Id]
	 */
	public static LinkedList<String> find3Hop(Long id1, Long id2, IdObject id1Object, IdObject id2bject)
			throws JSONException {
		System.out.println(5);
		LinkedList<String> _3Hop = new LinkedList<String>();
		if (id1Object.CId != 0) {
			Long[] ids = JsonTools.getRespId("And(RId=" + id2 + ",Composite(C.CId=" + id1Object.CId + "))", "Id");
			for (Long l : ids) {
				_3Hop.add("[" + id1 + "," + id1Object.CId + "," + l + "," + id2 + "]");
			}
		}

		if (id1Object.JId != 0) {
			Long[] ids = JsonTools.getRespId("And(RId=" + id2 + ",Composite(J.JId=" + id1Object.JId + "))", "Id");
			for (Long l : ids) {
				_3Hop.add("[" + id1 + "," + id1Object.JId + "," + l + "," + id2 + "]");
			}
		}
		return _3Hop;
	}

	/*
	 * 查找3-hop结果 3-hop:[Id,Id,C.CId,Id],[Id,Id,J.JId,Id]
	 */
	public static LinkedList<String> find3Hop2(Long id1, Long id2, IdObject id1Object, IdObject id2Object)
			throws JSONException {
		System.out.println(6);
		LinkedList<String> _3Hop = new LinkedList<String>();
		if (id2Object.CId != 0 && id1Object.RId != null && id1Object.RId.length != 0) {
			LinkedList<Long> ids = JsonTools.getRespIdList(otherIdUnion("C.CId", "Id", id1Object.RId, id2Object.CId), "Id");
			for (Long l : ids) {
				_3Hop.add("[" + id1 + "," + l + "," + id2Object.CId + "," + id2 + "]");
			}
		}

		if (id2Object.JId != 0 && id1Object.RId != null && id1Object.RId.length != 0) {
			LinkedList<Long> ids = JsonTools.getRespIdList(otherIdUnion("J.JId", "Id", id1Object.RId, id2Object.JId), "Id");
			for (Long l : ids) {
				_3Hop.add("[" + id1 + "," + l + "," + id2Object.JId + "," + id2 + "]");
			}
		}
		return _3Hop;
	}

	/*
	 * 查找3-hop结果
	 * 3-hop:[Id,Id,F.FId,Id],[Id,Id,AA.AuId,Id],[Id,F.FId,Id,Id],[Id,AA.AuId,Id
	 * ,Id]
	 */
	public static LinkedList<String> find3Hop3(Long id1, Long id2, IdObject id1Object, IdObject id2Object)
			throws JSONException {
		System.out.println(7);
		LinkedList<String> _3Hop = new LinkedList<String>();
		if (id2Object.FId != null && id1Object.RId.length != 0) {
			System.out.println("1");
			IdObject[] idObjects = JsonTools.getUnionResp(idUnion("Id", id1Object.RId));
			if (idObjects != null) {
				for (IdObject ob : idObjects) {
					if (ob.FId != null) {
						LinkedList<Long> FIds = intersection(ob.FId, id2Object.FId);
						if (FIds != null) {
							for (Long FId : FIds) {
								_3Hop.add("[" + id1 + "," + ob.Id + "," + FId + "," + id2 + "]");
							}
						}
					}
				}
			}

		}

		if (id2Object.AuId != null && id1Object.RId.length != 0) {
			System.out.println("2");
			IdObject[] idObjects = JsonTools.getUnionResp(idUnion("Id", id1Object.RId));
			if (idObjects != null) {
				for (IdObject ob : idObjects) {
					if (ob.AuId != null) {
						LinkedList<Long> AuIds = intersection(ob.AuId, id2Object.AuId);
						if (AuIds != null) {
							for (Long AuId : AuIds) {
								_3Hop.add("[" + id1 + "," + ob.Id + "," + AuId + "," + id2 + "]");
							}
						}
					}
				}
			}

		}

		if (id1Object.AuId != null) {
			System.out.println("3");
			Long[] id3 = JsonTools.getRespId("RId=" + id2, "Id");
			if (id3 != null && id3.length != 0) {
				LinkedList<String> list = idUnion("Id", id3);
				for (String s : list) {
					System.out.println(s);
				}
				IdObject[] idObjects = JsonTools.getUnionResp(idUnion("Id", id3));
				if (idObjects != null) {
					for (IdObject ob : idObjects) {
						if (ob.AuId != null) {
							LinkedList<Long> AuIds = intersection(ob.AuId, id1Object.AuId);
							if (AuIds != null) {
								for (Long AuId : AuIds) {
									_3Hop.add("[" + id1 + "," + AuId + "," + ob.Id + "," + id2 + "]");
								}
							}
						}
					}
				}
			}

		}

		if (id1Object.FId != null) {
			System.out.println("4");

			Long[] id3 = JsonTools.getRespId("RId=" + id2, "Id");
			if (id3 != null && id3.length != 0) {
				IdObject[] idObjects = JsonTools.getUnionResp(idUnion("Id", id3));
				if (idObjects != null) {
					for (IdObject ob : idObjects) {
						if (ob.FId != null) {
							LinkedList<Long> FIds = intersection(ob.FId, id1Object.FId);
							if (FIds != null) {
								for (Long FId : FIds) {
									_3Hop.add("[" + id1 + "," + FId + "," + ob.Id + "," + id2 + "]");
								}
							}
						}
					}
				}
			}

		}

		return _3Hop;
	}

	/*
	 * 查找3-hop结果 3-hop:[Id,Id,Id,Id]
	 */
	public static LinkedList<String> find3Hop4(Long id1, Long id2, IdObject id1Object, IdObject id2Object)
			throws JSONException {
		System.out.println(8);
		LinkedList<String> _3Hop = new LinkedList<String>();

		if (id1Object.RId != null && id1Object.RId.length != 0) {
			Long[] id3 = JsonTools.getRespId("RId=" + id2, "Id");
			sort(id3);

			if (id3 != null && id1Object.RId.length != 0 && id3.length != 0) {
				IdObject[] idObjects = JsonTools.getUnionResp(idUnion("Id", id1Object.RId));
				if (idObjects != null) {
					for (IdObject ob : idObjects) {
						if (ob.RId != null) {
							LinkedList<Long> RIds = intersection(ob.RId, id3);
							if (RIds != null) {
								for (Long RId : RIds) {
									_3Hop.add("[" + id1 + "," + ob.Id + "," + RId + "," + id2 + "]");
								}
							}
						}
					}
				}
			}

		}

		return _3Hop;
	}

	/*
	 * 用来联合数组中所有id 用于一条请求去查询所有id的信息
	 */
	public static LinkedList<String> idUnion(String name, Long[] a) {
		LinkedList<String> returnLinkedList = new LinkedList<String>();
		if (a.length < 100) {
			Queue<String> returnQueue = initUnion(name, a);
			while (returnQueue.size() > 1) {
				Queue<String> newQueue = new LinkedList<String>();
				newQueue.addAll(returnQueue);
				returnQueue.clear();
				returnQueue.addAll(union(newQueue));
			}
			returnLinkedList.add(returnQueue.poll());
		}else {
			Long[][] as = new Long[a.length/100+1][100];
			int length = a.length;
			int index = 0;
			while (length > 100) {
				for (int i = index * 100,j = 0;i<index*100+100;i++,j++) {
					as[index][j] = a[i];
				}
				index++;
				length-=100;
			}
			if (length != 0) {
				for (int i = 0,j = index*100;i<length;i++,j++) {
					as[index][i] = a[j];
				}
			}
			
			for (Long[] ls : as) {
				Queue<String> returnQueue = initUnion(name, ls);
				while (returnQueue.size() > 1) {
					Queue<String> newQueue = new LinkedList<String>();
					newQueue.addAll(returnQueue);
					returnQueue.clear();
					returnQueue.addAll(union(newQueue));
				}
				returnLinkedList.add(returnQueue.poll());

			}
		}
		return returnLinkedList;
	}


	/*
	 * 用来联合数组中所有id 用于一条请求去查询所有其它种类id的信息
	 */
	public static LinkedList<String> otherIdUnion(String comName, String IdName, Long[] a, Long Id) {
		LinkedList<String> returnLinkedList = new LinkedList<String>();
		System.out.println(a.length);
		if (a.length < 30) {
			Queue<String> returnQueue = initUnion2(comName, IdName, a, Id);
			while (returnQueue.size() > 1) {
				Queue<String> newQueue = new LinkedList<String>();
				newQueue.addAll(returnQueue);
				returnQueue.clear();
				returnQueue.addAll(union(newQueue));
			}
			returnLinkedList.add(returnQueue.poll());
		}else {
			Long[][] as = new Long[a.length/30+1][30];
			int length = a.length;
			int index = 0;
			while (length > 30) {
				for (int i = index * 30,j = 0;i<index*30+30;i++,j++) {
					as[index][j] = a[i];
				}
				index++;
				length-=30;
			}
			if (length != 0) {
				for (int i = 0,j = index*30;i<length;i++,j++) {
					as[index][i] = a[j];
				}
			}
			
			for (Long[] ls : as) {
				Queue<String> returnQueue = initUnion2(comName, IdName, ls, Id);
				while (returnQueue.size() > 1) {
					Queue<String> newQueue = new LinkedList<String>();
					newQueue.addAll(returnQueue);
					returnQueue.clear();
					returnQueue.addAll(union(newQueue));
				}
				returnLinkedList.add(returnQueue.poll());

			}
		}
		return returnLinkedList;
	}

	/*
	 * take the union
	 */
	public static LinkedList<Long> intersection(Long[] id1, Long[] id2) {
		if (id1 == null || id2 == null || id1.length == 0 || id2.length == 0) {
			return null;
		}
		LinkedList<Long> list = new LinkedList<Long>();
		int point1 = 0;
		int point2 = 0;
		while (point1 < id1.length && point2 < id2.length) {
			if (id1[point1] < id2[point2]&&!((id1[point1]+"").contains((id2[point2]+"")))) {
				point1++;
			} else if (id1[point1] > id2[point2]&&!((id1[point1]+"").contains((id2[point2]+"")))) {
				point2++;
			} else {
				if (id1[point1] != 0) {
					list.add(id1[point1]);
				}
				point1++;
				point2++;
			}
		}
		return list;
	}

	/*
	 * 初始化id联合查询的队列 eg:Id=123
	 */
	private static Queue<String> initUnion(String name, Long[] a) {
		Queue<String> baseQueue = new LinkedList<String>();
		for (Long l : a) {
			if (l!=null) {
				baseQueue.add(name + "=" + l);
			}else {
				break;
			}
		}
		return baseQueue;
	}


	/*
	 * 初始化id和其它种类id查询队列 eg:Id=123,Composite(AuId=123)
	 */
	private static Queue<String> initUnion2(String comName, String IdName, Long[] a, Long Id) {
		Queue<String> baseQueue = new LinkedList<String>();
		if (a!=null&&a.length!=0) {
			for (Long l : a) {
				if (l!=null) {
					baseQueue.add("And(" + IdName + "=" + l + "," + "Composite(" + comName + "=" + Id + "))");
				}else {
					break;
				}
			}
		}
		return baseQueue;
	}

	/*
	 * 按照查询格式，拼接字符串
	 */
	private static Queue<String> union(Queue<String> baseQueue) {
		Queue<String> returnQueue = new LinkedList<String>();
		while (baseQueue != null && baseQueue.size() != 0) {

			if (baseQueue.size() > 1) {
				returnQueue.add("Or(" + baseQueue.poll() + "," + baseQueue.poll() + ")");
			} else {
				returnQueue.add("Or(" + returnQueue.poll() + "," + baseQueue.poll() + ")");
			}
		}
		return returnQueue;
	}

	/*
	 * quick sort
	 */
	public static void sort(Comparable[] a) {
		if (a == null) {
			return;
		}
		sort(a, 0, a.length - 1);
	}

	private static void sort(Comparable[] a, int low, int high) {
		if (high < low) {
			return;
		}
		int j = partition(a, low, high);
		int k = j - 1;
		sort(a, low, j - 1);// 递归排序左半部分
		int m = j + 1;
		sort(a, j + 1, high);// 递归排序右半部分
	}

	private static int partition(Comparable[] a, int low, int high) {
		int i = low, j = high + 1;// 左右扫描指针
		Comparable v = a[low];// 切分元素
		while (true) {// 指针循环查找，直到左右指针重合
			while (i < high && less(a[++i], v)) {// 左指针向右查找比切分元素a[o]小的元素
				if (i == high) {
					break;
				}
			}
			while (j > low && less(v, a[--j])) {// 右指针向左查找比切分元素a[o]小的元素
				if (j == low) {
					break;
				}
			}
			if (i >= j) {
				break;
			}
			exch(a, i, j);
		}
		exch(a, low, j);
		return j;
	}

	private static void exch(Object[] a, int i, int j) {
		Object swap = a[i];
		a[i] = a[j];
		a[j] = swap;
	}

	private static boolean less(Comparable v, Comparable w) {
		return v.compareTo(w) < 0;
	}
}
