FROM eclipse-temurin:17-jdk-alpine
VOLUME /tmp
COPY target/*.jar app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
EXPOSE 8080

FROM maven:3-eclipse-temurin-17 AS build
COPY . .
RUN mvn clean package -holynekk
FROM eclipse-temurin:17-alpine
COPY --from=build /target/cengMarketplace-0.0.1-SNAPSHOT.jar mky-marketplace.jar
ENTRYPOINT ["java","-holynekk.profiles.active=render","-jar","mky-marketplace.jar"]