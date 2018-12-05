package mjaksic.distributed_system_client.service_communication;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.net.URISyntaxException;

import org.apache.http.HttpHeaders;
import org.apache.http.ParseException;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import com.google.gson.Gson;

import mjaksic.distributed_system_client.measurement.Measurement;

public class RESTInteractor {
	
	private static final CloseableHttpClient http_client = RESTInteractor.CreateHTTPClient();
	
	private static CloseableHttpClient CreateHTTPClient() {
		/**System.setProperty("org.apache.commons.logging.Log","org.apache.commons.logging.impl.SimpleLog");
		System.setProperty("org.apache.commons.logging.simplelog.showdatetime", "true");
		System.setProperty("org.apache.commons.logging.simplelog.log.org.apache.http.wire", "DEBUG");
		
		System.setProperty("org.apache.commons.logging.simplelog.log.org.apache.http.impl.conn", "DEBUG");
		System.setProperty("org.apache.commons.logging.simplelog.log.org.apache.http.impl.client", "DEBUG");
		System.setProperty("org.apache.commons.logging.simplelog.log.org.apache.http.client", "DEBUG");
		System.setProperty("org.apache.commons.logging.simplelog.log.org.apache.http", "DEBUG");
		*/
		return HttpClients.createDefault();
	}
	
	public static void Register(String id, SensorRegistration registration) {
		URI uri = RESTInteractor.BuildURI("http", "localhost:8080", "/sensor/" + id);
		HttpPut put_request = RESTInteractor.CreateHTTPPutter(uri);
		
		String json = RESTInteractor.CreateRegistrationString(registration);
		RESTInteractor.SetJSONContentType(put_request);
		RESTInteractor.SetJSONBody(put_request, json);
		
		CloseableHttpResponse response = RESTInteractor.ExecuteRequest(put_request);
		RESTInteractor.PrintResponse(response);
	}
	
	public static SensorAddress GetClosest(String id) {
		URI uri = RESTInteractor.BuildURI("http", "localhost:8080", "/sensor/" + id + "/closest");
		HttpGet get_request = RESTInteractor.CreateHTTPGetter(uri);
		
		RESTInteractor.SetJSONContentType(get_request);
		
		CloseableHttpResponse response = RESTInteractor.ExecuteRequest(get_request);
		//RESTInteractor.PrintResponse(response);
		
		SensorAddress address = RESTInteractor.GetAddressFromResponse(response);
		return address;
	}
	
	public static void StoreMeasurement(String id, Measurement measurement) {
		URI uri = RESTInteractor.BuildURI("http", "localhost:8080", "/sensor/" + id + "/measurement");
		HttpPut put_request = RESTInteractor.CreateHTTPPutter(uri);
		
		String json = RESTInteractor.CreateMeasurementString(measurement);
		RESTInteractor.SetJSONContentType(put_request);
		RESTInteractor.SetJSONBody(put_request, json);
		
		CloseableHttpResponse response = RESTInteractor.ExecuteRequest(put_request);
		RESTInteractor.PrintResponse(response);
	}
	
	
	
	/**
	 * 
	 * @param scheme Like "http"
	 * @param host Like "localhost"
	 * @param path Like "/sensor/26374829" 
	 * @return Like "http://localhost/sensor/26374829"
	 */
	private static URI BuildURI(String scheme, String host, String path) {
		URIBuilder builder = RESTInteractor.CreateURIBuilder();
		builder.setScheme(scheme).setHost(host).setPath(path);
		
		URI uri = null;
		try {
			uri = builder.build();
		} catch (URISyntaxException e) {
			e.printStackTrace();
		}
		return uri;
	}
	
	private static URIBuilder CreateURIBuilder() {
		return new URIBuilder();
	}
	
	
	
	private static HttpPut CreateHTTPPutter(URI uri) {
		return new HttpPut(uri);
	}
	
	private static HttpGet CreateHTTPGetter(URI uri) {
		return new HttpGet(uri);
	}
	
	
	
	private static String CreateRegistrationString(SensorRegistration registration) {
		Gson builder = RESTInteractor.CreateGson();
		String json = builder.toJson(registration);
		return json;
	}
	
	private static String CreateMeasurementString(Measurement measurement) {
		String json = "{\"temperature\":" + measurement.getTemperature() + ",\"pressure\":" + measurement.getPressure() + ",\"humidity\":" + measurement.getHumidity() + ",\"co\":" + measurement.getCO() + ",\"no2\":" + measurement.getNO2() + ",\"so2\":" + measurement.getSO2() + "}";
		return json;
	}
	
	private static Gson CreateGson() {
		return new Gson();
	}
	
	
	
	private static void SetJSONContentType(HttpUriRequest put_request) {
		put_request.setHeader(HttpHeaders.CONTENT_TYPE, "application/json");
	}
	
	private static void SetJSONBody(HttpPut put_request, String json) {
		try {
			put_request.setEntity(new StringEntity(json));
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
	}
	
	
	
	private static CloseableHttpResponse ExecuteRequest(HttpUriRequest request) {
		CloseableHttpResponse response = null;
		try {
			response = http_client.execute(request);
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return response;
	}
	
	private static void PrintResponse(CloseableHttpResponse response) {
		int status_code = RESTInteractor.GetStatusCode(response);
		String body = RESTInteractor.GetBody(response);
		
		System.out.println("--- Response ---");
		System.out.println("Status code: " + status_code);
		System.out.println("Body: " + body);
		System.out.println("--- ---  --- ---");
	}
	
	private static int GetStatusCode(CloseableHttpResponse response) {
		return response.getStatusLine().getStatusCode();
	}
	
	private static SensorAddress GetAddressFromResponse(CloseableHttpResponse response) {
		String body = RESTInteractor.GetBody(response);
		
		Gson gson = RESTInteractor.CreateGson();
		SensorAddress address = gson.fromJson(body, SensorAddress.class);
		return address;
	}
	
	private static String GetBody(CloseableHttpResponse response) {
		String string = null;
		try {
			string = EntityUtils.toString(response.getEntity());
		} catch (ParseException e) {
			System.out.println("Error parsing body");
			e.printStackTrace();
		} catch (IOException e) {
			System.out.println("Error IO error");
			e.printStackTrace();
		};
		return string;
	}
}
