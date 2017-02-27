package sgd;

import java.util.LinkedList;

public class Result {
	public static LinkedList<String> myResult = new LinkedList<String>();
	
	public static String getResult(LinkedList<String> l) {
		String result= "[";
		if (l.size()==0) {
			return "[]";
		}else{
			for (int i = 0;i<l.size()-1;i++) {
				result+=l.get(i)+",";
			}
			result+=l.get(l.size()-1)+"]";
			return result;
		}
	}
}
