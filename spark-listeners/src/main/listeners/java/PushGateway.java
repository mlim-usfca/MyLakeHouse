package listeners;

import io.prometheus.client.Gauge;
import listeners.CustomizedListener;
import scala.collection.Iterator;
import scala.collection.immutable.Set;
import io.prometheus.client.CollectorRegistry;

import java.io.IOException;

public class PushGateway {
    public static void push(Set<String> applicationSet) {
        System.out.println("pushgateway + " + applicationSet);

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

        System.out.println(registry);
        // Push metrics to the Pushgateway
        io.prometheus.client.exporter.PushGateway pushGateway = new io.prometheus.client.exporter.PushGateway("127.0.0.1:9091");

        try {
            pushGateway.pushAdd(registry, "my_job");
            System.out.println("Successfully pushed my_job");
        } catch (IOException e) {
            System.out.println("Error pushing metrics to Pushgateway:");
            e.printStackTrace();
            System.out.println("Error message: " + e.getMessage());
        }
    }
}
