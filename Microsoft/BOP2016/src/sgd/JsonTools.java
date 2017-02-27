package sgd;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class JsonTools {
	public static Map<Long, String> getAA(JSONArray entitiesArray, JSONArray entitiesArray2) throws JSONException {
		Map<Long, String> myAA = new HashMap<Long, String>();
		for (int i = 0; i < entitiesArray.length(); i++) {
			JSONObject entitiesObject = entitiesArray.getJSONObject(i);
			JSONArray AAArray = entitiesObject.getJSONArray("AA");
			if (AAArray != null && AAArray.length() != 0) {
				for (int j = 0; j < AAArray.length(); j++) {
					JSONObject AAObject = AAArray.getJSONObject(j);
					if (!AAObject.isNull("AuId") && !AAObject.isNull("AfId")) {
						myAA.put(AAObject.getLong("AuId"),
								myAA.get(AAObject.getLong("AuId")) + "," + AAObject.getLong("AfId"));
					}
				}
			}
		}

		for (int i = 0; i < entitiesArray2.length(); i++) {
			JSONObject entitiesObject2 = entitiesArray2.getJSONObject(i);
			JSONArray AAArray2 = entitiesObject2.getJSONArray("AA");
			if (AAArray2 != null && AAArray2.length() != 0) {
				for (int j = 0; j < AAArray2.length(); j++) {
					JSONObject AAObject2 = AAArray2.getJSONObject(j);
					if (!AAObject2.isNull("AuId") && !AAObject2.isNull("AfId")) {
						myAA.put(AAObject2.getLong("AuId"),
								myAA.get(AAObject2.getLong("AuId")) + "," + AAObject2.getLong("AfId"));
					}
				}
			}
		}
		return myAA;

	}

	public static IdObject[] getUnionResp(LinkedList<String> reqs) throws JSONException {
		LinkedList<IdObject> IdObjectList = new LinkedList<IdObject>();
		LinkedList<String> result = new LinkedList<String>();
		if (reqs != null && reqs.size() > 2) {
			getFirstResult(reqs, "Id,RId,AA.AuId,AA.AfId,F.FId,J.JId,C.CId", result);
			for (String req : result) {
				if (req != null) {
					JSONObject json = new JSONObject(req);
					JSONArray entitiesArray = json.getJSONArray("entities");
					for (int i = 0; i < entitiesArray.length(); i++) {
						IdObjectList.add(getIdObject(entitiesArray.getJSONObject(i)));
					}
				}
			}
		} else {
			for (String req : reqs) {
				if (req != null) {
					JSONObject json = new JSONObject(
							GetAPI.getEvaluate(req, "10000", "Id,RId,AA.AuId,AA.AfId,F.FId,J.JId,C.CId"));
					JSONArray entitiesArray = json.getJSONArray("entities");
					for (int i = 0; i < entitiesArray.length(); i++) {
						IdObjectList.add(getIdObject(entitiesArray.getJSONObject(i)));
					}
				}
			}
		}

		IdObject[] idObjects = new IdObject[IdObjectList.size()];
		for (int i = 0; i < IdObjectList.size(); i++) {
			idObjects[i] = IdObjectList.get(i);
		}
		return idObjects;
	}

	public static Long[] getRespId(String req, String intent) throws JSONException {
		JSONObject json = new JSONObject(GetAPI.getEvaluate(req, "10000", intent));
		JSONArray entitiesArray = json.getJSONArray("entities");
		Long[] Ids = new Long[entitiesArray.length()];
		for (int i = 0; i < Ids.length; i++) {
			Ids[i] = entitiesArray.getJSONObject(i).getLong("Id");
		}
		return Ids;
	}

	public static LinkedList<Long> getRespIdList(LinkedList<String> req, String intent) throws JSONException {
		LinkedList<Long> returnList = new LinkedList<Long>();
		LinkedList<String> result = new LinkedList<String>();
		if (req != null && req.size() > 2) {
			getFirstResult(req, intent, result);
			for (String re:result) {
				JSONObject json = new JSONObject(re);
				JSONArray entitiesArray = json.getJSONArray("entities");
				for (int i = 0;i<entitiesArray.length();i++) {
					returnList.add(entitiesArray.getJSONObject(i).getLong("Id"));
				}

			}
			
		}else if (req!=null&req.size()!=0) {
			for (String reqs:req) {
				JSONObject json = new JSONObject(GetAPI.getEvaluate(reqs, "10000", intent));
				JSONArray entitiesArray = json.getJSONArray("entities");
				for (int i = 0;i<entitiesArray.length();i++) {
					returnList.add(entitiesArray.getJSONObject(i).getLong("Id"));
				}
			}
		}
		return returnList;
	}

	public static IdObject getIdObject(JSONObject entitiesJSONObject) throws JSONException {
		int RIdLength = 0, AuIdLength = 0, AfIdLength = 0, FIdLength = 0;
		Long CId = 0L, JId = 0L, Id = 0L;
		Id = entitiesJSONObject.getLong("Id");
		if (entitiesJSONObject.isNull("J")) {
			JId = 0L;
		} else {
			JId = entitiesJSONObject.getJSONObject("J").getLong("JId");
		}

		if (entitiesJSONObject.isNull("C")) {
			CId = 0L;
		} else {
			CId = entitiesJSONObject.getJSONObject("C").getLong("CId");
		}

		if (entitiesJSONObject.isNull("RId")) {
			RIdLength = 0;
		} else {
			RIdLength = entitiesJSONObject.getJSONArray("RId").length();
		}

		if (entitiesJSONObject.isNull("AA")) {
			AuIdLength = 0;
			AfIdLength = 0;
		} else {
			JSONArray AAJSONArray = entitiesJSONObject.getJSONArray("AA");
			for (int i = 0; i < AAJSONArray.length(); i++) {
				if (!AAJSONArray.getJSONObject(i).isNull("AuId")) {
					AuIdLength++;
				}
				if (!AAJSONArray.getJSONObject(i).isNull("AfId")) {
					AfIdLength++;
				}
			}
		}
		if (entitiesJSONObject.isNull("F")) {
			FIdLength = 0;
		} else {
			JSONArray FJSONArray = entitiesJSONObject.getJSONArray("F");
			FIdLength = FJSONArray.length();
		}
		IdObject idObject = new IdObject(RIdLength, AuIdLength, AfIdLength, FIdLength, CId, JId, Id);
		if (RIdLength != 0) {
			for (int i = 0; i < RIdLength; i++) {
				idObject.RId[i] = entitiesJSONObject.getJSONArray("RId").getLong(i);
			}
			Compute.sort(idObject.RId);
		}
		if (AuIdLength != 0 || AfIdLength != 0) {
			int auindex = 0;
			int afindex = 0;
			JSONArray AAJSONArray = entitiesJSONObject.getJSONArray("AA");
			for (int i = 0; i < AAJSONArray.length(); i++) {
				if (!AAJSONArray.getJSONObject(i).isNull("AuId")) {
					idObject.AuId[auindex] = AAJSONArray.getJSONObject(i).getLong("AuId");
					auindex++;
				}
				if (!AAJSONArray.getJSONObject(i).isNull("AfId")) {
					idObject.AfId[afindex] = AAJSONArray.getJSONObject(i).getLong("AfId");
					afindex++;
				}
			}
			Compute.sort(idObject.AfId);
			Compute.sort(idObject.AuId);

		}
		if (FIdLength != 0) {
			JSONArray FJSONArray = entitiesJSONObject.getJSONArray("F");
			for (int i = 0; i < FJSONArray.length(); i++) {
				idObject.FId[i] = FJSONArray.getJSONObject(i).getLong("FId");
			}
			Compute.sort(idObject.FId);
		}

		return idObject;
	}

	public static IdObject[] getAuIdObject(JSONArray entitiesArray) throws JSONException {
		IdObject[] idObjects = new IdObject[entitiesArray.length()];
		for (int j = 0; j < idObjects.length; j++) {
			int RIdLength = 0, AuIdLength = 0, AfIdLength = 0, FIdLength = 0;
			Long CId = 0L, JId = 0L, Id = 0L;
			JSONObject entitiesJSONObject = entitiesArray.getJSONObject(j);
			Id = entitiesJSONObject.getLong("Id");
			if (entitiesJSONObject.isNull("J")) {
				JId = 0L;
			} else {
				JId = entitiesJSONObject.getJSONObject("J").getLong("JId");
			}

			if (entitiesJSONObject.isNull("C")) {
				CId = 0L;
			} else {
				CId = entitiesJSONObject.getJSONObject("C").getLong("CId");
			}

			if (entitiesJSONObject.isNull("RId")) {
				RIdLength = 0;
			} else {
				RIdLength = entitiesJSONObject.getJSONArray("RId").length();
			}

			if (entitiesJSONObject.isNull("AA")) {
				AuIdLength = 0;
				AfIdLength = 0;
			} else {
				JSONArray AAJSONArray = entitiesJSONObject.getJSONArray("AA");
				for (int i = 0; i < AAJSONArray.length(); i++) {
					if (!AAJSONArray.getJSONObject(i).isNull("AuId")) {
						AuIdLength++;
					}
					if (!AAJSONArray.getJSONObject(i).isNull("AfId")) {
						AfIdLength++;
					}
				}
			}
			if (entitiesJSONObject.isNull("F")) {
				FIdLength = 0;
			} else {
				JSONArray FJSONArray = entitiesJSONObject.getJSONArray("F");
				FIdLength = FJSONArray.length();
			}

			idObjects[j] = new IdObject(RIdLength, AuIdLength, AfIdLength, FIdLength, CId, JId, Id);
			if (RIdLength != 0) {
				for (int i = 0; i < RIdLength; i++) {
					idObjects[j].RId[i] = entitiesJSONObject.getJSONArray("RId").getLong(i);
				}
				Compute.sort(idObjects[j].RId);
			}
			if (AuIdLength != 0 || AfIdLength != 0) {
				int auindex = 0;
				int afindex = 0;
				JSONArray AAJSONArray = entitiesJSONObject.getJSONArray("AA");
				for (int i = 0; i < AAJSONArray.length(); i++) {
					if (!AAJSONArray.getJSONObject(i).isNull("AuId")) {
						idObjects[j].AuId[auindex] = AAJSONArray.getJSONObject(i).getLong("AuId");
						auindex++;
					}
					if (!AAJSONArray.getJSONObject(i).isNull("AfId")) {
						idObjects[j].AfId[afindex] = AAJSONArray.getJSONObject(i).getLong("AfId");
						afindex++;
					}
				}
				Compute.sort(idObjects[j].AfId);
				Compute.sort(idObjects[j].AuId);

			}
			if (FIdLength != 0) {
				JSONArray FJSONArray = entitiesJSONObject.getJSONArray("F");
				for (int i = 0; i < FJSONArray.length(); i++) {
					idObjects[j].FId[i] = FJSONArray.getJSONObject(i).getLong("FId");
				}
				Compute.sort(idObjects[j].FId);
			}
		}
		return idObjects;
	}

	private static LinkedList<String> getFirstResult(List<String> query, String attribute, LinkedList<String> result) {

		for (String s : query) {
			new ReqThread(s, attribute, result).start();
		}

		while (result.size() < query.size()) {
			System.out.println(result.size() + "\t" + query.size());
		}

		return result;
	}

	/*
	 * 最后的调试——1
	 */
	public static void Id2AuIdByThread(IdObject[] idObjects, IdObject idObject, Long id1, Long AuId,
			LinkedList<String> result) {
		LinkedList<String> index = new LinkedList<String>();
		for (IdObject ob : idObjects) {
			new ReqAndComThread("RId=" + ob.Id, id1, AuId, idObject, result, index).start();
		}
		while (index.size() < idObjects.length) {
			System.out.println(index.size() + "\t" + idObjects.length);
		}
	}
}
