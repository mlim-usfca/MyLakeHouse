import io.prometheus.client.Gauge;
import listeners.CustomizedListener;
import scala.collection.Iterator;
import scala.collection.immutable.Set;
import io.prometheus.client.CollectorRegistry;
import io.prometheus.client.exporter.PushGateway;

import java.io.IOException;

public class PushGatewayer {
    public static void main(String[] args) {
        Set<String> applicationSet = CustomizedListener.getApplicationSet();
        System.out.println(applicationSet);

        // Create a CollectorRegistry
        CollectorRegistry registry = new CollectorRegistry();

        // Create a Gauge metric
        Gauge gauge = Gauge.build()
                .name("my_custom_metric")
                .help("Description of my custom metric")
                .labelNames("element")
                .register(registry);

        // Set the value of the Gauge metric
        Iterator<String> iterator = applicationSet.iterator();
        while (iterator.hasNext()) {
            String element = iterator.next();
            gauge.labels(element).set(1);
        }

        // Push metrics to the Pushgateway
        PushGateway pushGateway = new PushGateway("http://pushgateway.example.com:9091");
        try {
            pushGateway.pushAdd(registry, "my_job");
            System.out.println("Successfully pushed my_job");
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
}
