package sgd;

import java.util.LinkedList;

public class ReqThread extends Thread{

	public boolean isEnd = false;
	public String content = "";
	public String attributes = "";
	public LinkedList<String> result;
	public ReqThread(String content,String attributes,LinkedList<String> result) {
		this.content = content;
		this.result = result;
		this.attributes = attributes;
	}
	@Override
	public void run(){
		while (!isEnd) {
			String s = GetAPI.getEvaluate(content, "10000", attributes);
			result.add(s);
			isEnd = true;
		}
	}
}
