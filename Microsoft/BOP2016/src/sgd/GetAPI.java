/*
 * Call API by used get request Class
 */
package sgd;


import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class GetAPI {
	
	public final static String SUBSCRIPTION_KEY = "f7cc29509a8443c5b3a5e56b0e38b5a6";
	
	public static String getEvaluate(String content,String count,String attributes) {
		if (content != null) {
			return sendGet("evaluate", content, count, attributes,SUBSCRIPTION_KEY);
		}else {
			return null;
		}
	}
	
	private static String sendGet(String api,String content,String count,String attributes,String key) {
		String result = "";
		BufferedReader in = null;
		try {
			URL realUrl = new URL("https://oxfordhk.azure-api.net/academic/v1.0/"+api
					+"?expr="+content
					+"&count="+count
					+"&attributes="+attributes
					+"&subscription-key=" + key);//����������ƴ������get����ת��URL��
			System.out.println("get"+realUrl);
			HttpURLConnection connection = (HttpURLConnection) realUrl.openConnection();//��������
			connection.connect();//��ʼ����
			in = new BufferedReader(new InputStreamReader(connection.getInputStream(), "UTF-8"));
			String line;
			while ((line = in.readLine()) != null) {
				result += line + "\n";//ע������\n����ƥ����ܻ����
			}
		} catch (Exception e) {//�쳣����
			System.out.println("����get�������");
			e.printStackTrace();
		} finally {
			try {
				if (in != null) {
					in.close();
				}
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		return result;
	}
}
