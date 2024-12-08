# Use a Maven image to build the application
FROM maven:3.8.4-openjdk-11-slim AS build

# Set the working directory
WORKDIR /app

# Copy the Maven project files into the container
COPY pom.xml .
COPY src ./src

# Build the application using Maven
RUN mvn clean package -DskipTests

# Use a standard OpenJDK runtime
FROM openjdk:17

# Set the working directory in the runtime image
WORKDIR /app

# Copy the JAR file from the build stage
COPY --from=build /app/target/*-jar-with-dependencies.jar app.jar

# Expose the application port (optional)
EXPOSE 8080

# Set the command to run the application
CMD ["java", "-jar", "app.jar"]