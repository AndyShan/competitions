package com.test.action;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.LinkedList;
import java.util.Map;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import sgd.Compute;
import sgd.ComputeAuId2AuId;
import sgd.ComputeAuId2Id;
import sgd.ComputeId2AuId;
import sgd.GetAPI;
import sgd.IdObject;
import sgd.JsonTools;
import sgd.Result;

public class TestServlet extends HttpServlet {

@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException
	{
	
		String s =req.getParameter("id1");//获取id参数
		Long id1 = Long.parseLong(s);
//		System.out.println("!!!!!"+id1);

		String s2 =req.getParameter("id2");
		Long id2 = Long.parseLong(s2);
//		System.out.println("!!!!!"+id2);
		
		LinkedList<String> finalResult = new LinkedList<String>();
		
		
		
		
		
		try {
			String result = isId(id1);//判断是id还是AuId
			String result2 = isId(id2);
			if (result!=null&&result2!=null) {//Id->Id
//				System.out.println(result);
//				System.out.println(result2);
				JSONObject json = new JSONObject(result);//解析返回 的json字符串
				JSONArray entitiesArray = json.getJSONArray("entities");
				JSONObject entitiesArrayObject = entitiesArray.getJSONObject(0);

				JSONObject json2 = new JSONObject(result2);
				JSONArray entitiesArray2 = json2.getJSONArray("entities");
				JSONObject entitiesArrayObject2 = entitiesArray2.getJSONObject(0);
				IdObject my1 = sgd.JsonTools.getIdObject(entitiesArrayObject);//缓存解析的内容到IdObject中
				IdObject my2 = sgd.JsonTools.getIdObject(entitiesArrayObject2);
				finalResult = Compute.findHop(id1,id2,my1, my2);//计算

			}else if (result==null&&result2!=null) {//AuId->Id
				result = GetAPI.getEvaluate("Composite(AA.AuId="+id1+")", "1000", "RId,Id,F.FId,J.JId,C.CId,AA.AuId,AA.AfId");
//				System.out.println(result);
//				System.out.println(result2);
				
				JSONObject json = new JSONObject(result);
				JSONArray entitiesArray = json.getJSONArray("entities");
				JSONObject json2 = new JSONObject(result2);
				JSONArray entitiesArray2 = json2.getJSONArray("entities");
				JSONObject entitiesArrayObject2 = entitiesArray2.getJSONObject(0);
				
				Map<Long,String> myAA = JsonTools.getAA(entitiesArray, entitiesArray2);//将解析的AA先关的信息存入(AuId:AfId)map
				IdObject[] id1Objects = sgd.JsonTools.getAuIdObject(entitiesArray);
				IdObject id2Object = sgd.JsonTools.getIdObject(entitiesArrayObject2);
				finalResult = ComputeAuId2Id.findHop(id1, id2, id1Objects, id2Object,myAA);
			}else if (result==null&&result2==null) {//AuId->AuId
				result = GetAPI.getEvaluate("Composite(AA.AuId="+id1+")", "1000", "RId,Id,F.FId,J.JId,C.CId,AA.AuId,AA.AfId");
//				System.out.println(result);
				result2 = GetAPI.getEvaluate("Composite(AA.AuId="+id2+")", "1000", "RId,Id,F.FId,J.JId,C.CId,AA.AuId,AA.AfId");
//				System.out.println(result2);
				JSONObject json = new JSONObject(result);
				JSONArray entitiesArray = json.getJSONArray("entities");
				JSONObject json2 = new JSONObject(result2);
				JSONArray entitiesArray2 = json2.getJSONArray("entities");
				IdObject[] id1Objects = sgd.JsonTools.getAuIdObject(entitiesArray);
				IdObject[] id2Objects = sgd.JsonTools.getAuIdObject(entitiesArray2);
				Map<Long,String> myAA = sgd.JsonTools.getAA(entitiesArray, entitiesArray2);
				finalResult = ComputeAuId2AuId.findHop(id1,id2, id1Objects, id2Objects,myAA);

			}else if (result!=null&&result2==null) {//Id->AuId
				System.out.println(result);
				result2 = GetAPI.getEvaluate("Composite(AA.AuId="+id2+")", "1000", "RId,Id,F.FId,J.JId,C.CId,AA.AuId,AA.AfId");
				System.out.println(result2);

				JSONObject json = new JSONObject(result);
				JSONArray entitiesArray = json.getJSONArray("entities");
				JSONObject entitiesArrayObject = entitiesArray.getJSONObject(0);
				JSONObject json2 = new JSONObject(result2);
				JSONArray entitiesArray2 = json2.getJSONArray("entities");
				
				IdObject id1Object = sgd.JsonTools.getIdObject(entitiesArrayObject);
				IdObject[] id2Objects = sgd.JsonTools.getAuIdObject(entitiesArray2);
				Map<Long,String> myAA = sgd.JsonTools.getAA(entitiesArray, entitiesArray2);

				finalResult = ComputeId2AuId.findHop(id1, id2, id1Object, id2Objects,myAA);

				
			}
		} catch (JSONException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}


		

		System.out.println("-------------");
		//直接返回
		PrintWriter pw = resp.getWriter();
		if (finalResult != null) {
			System.out.println(finalResult.size());
			pw.println(Result.getResult(finalResult));
		}else {
			pw.println("[]");

		}

		pw.close();
		System.out.println("-------------");

	}

	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException
	{
		// TODO Auto-generated method stub
		doGet(req, resp);
	}
	
	public static String isId(Long id) throws JSONException {//判断id种类的方法
		String result = GetAPI.getEvaluate("Id="+id, "1000", "RId,Id,F.FId,J.JId,C.CId,AA.AuId,AA.AfId");
		JSONObject json = new JSONObject(result);
		JSONArray entitiesArray = json.getJSONArray("entities");
		if (!entitiesArray.isNull(0)) {
			JSONObject entitiesJSONObject = entitiesArray.getJSONObject(0);
			if (entitiesJSONObject.isNull("AA")) {
				result = null;
			}
		}
		
		return result;
	}
}
