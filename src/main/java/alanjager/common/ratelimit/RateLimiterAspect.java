// Created by AlanJager on 2016/10/27.
package alanjager.common.ratelimit;

import com.google.common.base.Strings;
import com.google.common.util.concurrent.RateLimiter;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Function;

@Aspect
@Component
public class RateLimiterAspect {
    public interface KeyFactory {
        String createKey(JoinPoint joinPoint, RateLimit rateLimit);
    }

    private static final Logger LOGGER = LoggerFactory.getLogger(RateLimiterAspect.class);

    private static final KeyFactory DEFAULT_KEY_FACTORY = (joinPoint, rateLimit) -> JoinPointToStringHelper.toString(joinPoint);

    private final ConcurrentHashMap<String, RateLimiter> limiters;
    private final KeyFactory keyFactory;

    @Autowired
    public RateLimiterAspect(Optional<KeyFactory> keyFactory)
    {
        this.limiters = new ConcurrentHashMap<>();
        this.keyFactory = keyFactory.orElse(DEFAULT_KEY_FACTORY);
    }

    @Before("@annotation(rateLimit)")
    public void rateLimit(JoinPoint joinPoint, RateLimit rateLimit)
    {
        String key = createKey(joinPoint, rateLimit);
        RateLimiter limiter = limiters.computeIfAbsent(key, createLimiter(rateLimit));
        double delay = limiter.acquire();
        LOGGER.debug("Acquired rate limit permission ({} qps) for {} in {} seconds", limiter.getRate(), key, delay);
        // test information
        LOGGER.info("rate limit in working");
    }

    private Function<String, RateLimiter> createLimiter(RateLimit rateLimit)
    {
        return name -> RateLimiter.create(rateLimit.value());
    }

    private String createKey(JoinPoint joinPoint, RateLimit rateLimit)
    {
        return Optional.ofNullable(Strings.emptyToNull(rateLimit.key()))
                .orElseGet(() -> keyFactory.createKey(joinPoint, rateLimit));
    }
}
