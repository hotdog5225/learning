import org.jsoup.Jsoup;
import org.jsoup.nodes.*;
import org.jsoup.select.Elements;

import java.io.IOException;

// one file only and must has a public CLass
public class HelloWorld {
    public static void main(String[] args) throws IOException {
        System.out.println("hello world");
        String url = "http://www.baidu.com";
        Document doc = Jsoup.connect(url).get();
        Elements links = doc.select("a[href]");
        for (Element link : links) {
            String linkHref = link.attr("href");
            System.out.println(linkHref);
        }
    }
}
