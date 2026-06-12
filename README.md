# RTSDK Java Maven Pom file Generator (using Python)
- version: 1.0
- Last update: June 2026
- Environment: Windows
- Prerequisite: [Prerequisite](#prerequisite)

## <a id="Introduction"></a>Introduction

[LSEG Real-Time SDK (Java Edition)](https://developers.lseg.com/en/api-catalog/refinitiv-real-time-opnsrc/rt-sdk-java) (RTSDK, formerly known as Elektron SDK) is a suite of modern and open source APIs that aim to simplify development through a strong focus on ease of use and standardized access to a broad set of Refinitiv proprietary content and services via the proprietary TCP connection named RSSL and proprietary binary message encoding format named OMM Message. The capabilities range from low latency/high-performance APIs right through to simple streaming Web APIs. 

The SDK has been released on the [Maven Central Repository](https://central.sonatype.com/) to support the modern Java development life cycle since the RTSDK Java (formerly known as Elektron SDK) version 1.2. The Maven Central Repository supported also lets SDK compatibilities with the Java build automation tools like [Gradle](https://gradle.org/) and [Apache Maven](https://maven.apache.org/). This helps Java developers to build RTSDK Java applications, manage its dependencies (Java Developers do not need to manually manage different versions of jar files anymore), and better collaboration in the team.

The RTSDK Java package comes with the Gradle build tool supported by default. Some developers who are using Maven might feel difficult to try the SDK example codes in their Maven development workflow. 

To make Maven developers life easier, I am creating simple tool for generating RTSDK Java Examples Maven's pom.xml file to run the RTSDK Java example source code. The tool supports RTSDK Java since the rebranding version 2.0.0.L1 (EMA/ETA 3.6.0), and you can customize the configuration file to make it supports the future versions of the SDK.

### Caution

The generated pom.xml file is for running EMA or ETA APIs examples only. The file is **not optimized and not recommended for the Production use!**. I am not provide any supports for this simple tool.

## <a id="prerequisite"></a>Prerequisite

All scripts require [Python](https://www.python.org/) compiler to run.

The application logic of this tool is simple enough that you can re-create in other programming language. I am choosing Python because its simplicity (and friendly for my company beloved ZScaler).

This project is a Python version of my [RTSDK Java Maven Pom file Generator (using Ruby)](https://github.com/LSEG-API-Samples/Example.RTSDK.Java.MavenPomGenerator) project.

## <a id="rtsdkj_maven"></a>Maven pom.xml setting for RTSDK Java

The ```pom.xml``` file the main Maven's project configuration. This XML file contains the information required to build a project.

### Maven pom.xml file for EMA Java Examples

The EMA API Java edition has two type of example applications as follows:
- console example applications in the *training* folder (for Consumer, Interactive Provider, and Non-Interactive Provider applications)
- GUI consumer example application in the *rrtmdviewer** folder.

The GUI example needs [JavaFX](https://openjfx.io/) dependency, so the pom.xml file need JavaFX dependency information too.

You can specify the following EMA Java API and JavaFX dependencies in the Maven pom.xml file for running the EMA Java example applications.

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    ...
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
    <rtsdk.version>3.7.2.0</rtsdk.version>
    <javafx.version>15.0.1</javafx.version>
</properties>

    <dependencies>
        <!-- RTSDK -->
        <!-- For EMA Java Project -->
        <dependency>
            <groupId>com.refinitiv.ema</groupId>
            <artifactId>ema</artifactId>
            <version>${rtsdk.version}</version>
        </dependency>
    </dependencies>
    <dependency>
			<groupId>org.openjfx</groupId>
			<artifactId>javafx-fxml</artifactId>
			<version>${javafx.version}</version>
		</dependency>
		<dependency>
			<groupId>org.openjfx</groupId>
			<artifactId>javafx-controls</artifactId>
			<version>${javafx.version}</version>
		</dependency>
</project>
```

### Maven pom.xml file for ETA Java Examples

The pom.xml file for the ETA Java application is the following. The Maven can automatic pull ETA, ETA ValueAdd and ETA JSON Converter artifacts within Maven central for the application with the ```com.refinitiv.eta.valueadd.cache``` dependency declaration.

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    ...
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
	<maven.compiler.source>25</maven.compiler.source>
	<maven.compiler.target>25</maven.compiler.target>
	<rtsdk.version>3.10.0.1</rtsdk.version>
	<javafx.version>25.0.3</javafx.version>
</properties>
    <!-- RTSDK -->
    <!-- For ETA Java Project -->
    <dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>4.11</version>
			<scope>compile</scope>
		</dependency>
        
		<dependency>
			<groupId>org.mockito</groupId>
			<artifactId>mockito-core</artifactId>
			<version>1.9.5</version>
		</dependency>
		<dependency>
			<groupId>com.refinitiv.eta.valueadd.cache</groupId>
			<artifactId>etaValueAddCache</artifactId>
			<version>${rtsdk.version}</version>
		</dependency>
		<dependency>
			<groupId>com.refinitiv.eta.ansi</groupId>
			<artifactId>ansipage</artifactId>
			<version>${rtsdk.version}</version>
		</dependency>
</project>
```

## How to add new RTSDK Java version

The RTSDK Java version detail is available in the ```config/rtsdk_versions.yaml``` file in the YAML format as follows:

``` YAML
--- # RTSDK Version Mapping
rtsdk_versions:
  2.1.0: '3.7.0.0'
  2.1.1: '3.7.1.0'
  2.1.2: '3.7.2.0'
  2.1.3: '3.7.3.0'

latest_version: '2.4.0'
```

You can add more versions by add the RTSDK Java version as a Key (```2.2.0```, ```2.2.1```, and so on), then add the [EMA/ETA Java Maven Central](https://central.sonatype.com/?smo=true) version as a string value. The EMA/ETA Java Maven Central version number is available on the *# Maven Central* section of the RTSDK Java's README file and the [Maven Central](https://central.sonatype.com/?smo=true) website.

**Update Nov 2022**: 
- For RTSDK version 2.0.7.**L2**, please specify the RTSDK version as **3.6.7.3** in the pom.xml file.

Example *with dummy versions*:
``` YAML
--- # RTSDK Version Mapping
rtsdk_versions:
  2.0.7: '3.6.7.3'
  2.0.8: '3.6.8.0'
  3.0.1: '4.7.1.0' 

latest_version: '3.0.1'
```

## How to add new Supported JDK and JavaFX version

The supported JDK and JavaFX versions are consolidated in the ```config/rtsdk_versions.yaml``` file in the YAML format as follows:

```YAML
support_jdk_jfx_versions:
  11: '17.0.19'
  17: '21.0.11'
  21: '21.0.11'
  25: '25.0.3'
```

Each JDK version maps to its compatible JavaFX version. This consolidated structure makes it clear that JDK and JavaFX versions are tightly coupled.

Please refer to the [RTSDK Java Readme file](https://github.com/Refinitiv/Real-Time-SDK/blob/master/Java/README.md), [Change Log](https://github.com/Refinitiv/Real-Time-SDK/blob/master/Java/CHANGELOG.md), and [Java FX Roadmap and LTS releases](https://gluonhq.com/products/javafx/) to add new JDK/JavaFX pairs.

Example *with dummy versions*:

```YAML
support_jdk_jfx_versions:
  11: '17.0.19'
  17: '21.0.11'
  21: '21.0.11'
  25: '25.0.3'
  26: '26.0.1'
```

## How to Use with Python

1. Open a Command Prompt and go to project's folder
2. Run the following command in a Command Prompt to create a Python virtual environment named *venv* for the project.

    ```bash
    $>python -m venv venv
    ```

3. Once the environment is created, activate a virtual environment named ```venv``` with this command in a Command Prompt

    ```bash
    $>venv\Scripts\activate
    ```

4. Run the following command in a Command Prompt to install the project dependencies

    ```bash
    $>(venv)> pip install -r requirements.txt
    ```

5. Run the *maven_pom_generator.py* script with the following command line argument:

    ```bash
    $>(venv)>python maven_pom_generator.py --api <EMA (default)/ETA> --version <RTSDK version, ex 2.0.8>
    ```

6. The result ```pom.xml``` file will be generated in the ```output``` folder.

Example result:
```Bash
(venv)$>python maven_pom_generator.py --api EMA --version 2.4.0
API version: 3.10.0.1
Java SDK: 17
JavaFX SDK: 21.0.11
Generated: ./output/pom.xml
```

## Testing

This project includes a comprehensive test suite using [pytest](https://pytest.org/). The test suite validates all functionality with 96% code coverage and 68 passing tests.
Run tests only in the same activated project virtual environment from the "How to Use with Python" section, not with global Python or global pytest.

### Running Tests

```bash
# Run all tests
(venv)$>python -m pytest tests/ -v

# Run tests with coverage report (generates htmlcov/index.html)
(venv)$>python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

# Run specific test module
(venv)$>python -m pytest tests/test_config_loading.py -v
(venv)$>python -m pytest tests/test_argument_parser.py -v
(venv)$>python -m pytest tests/test_sdk_context.py -v
(venv)$>python -m pytest tests/test_template_rendering.py -v
(venv)$>python -m pytest tests/test_integration.py -v

# Run tests matching a pattern
(venv)$>python -m pytest tests/ -k "jdk" -v
(venv)$>python -m pytest tests/ -k "ema" -v
```

### Test Coverage

| Module | Tests | Coverage |
|--------|-------|----------|
| test_config_loading.py | 9 | 100% |
| test_argument_parser.py | 18 | 100% |
| test_sdk_context.py | 18 | 100% |
| test_template_rendering.py | 15 | 100% |
| test_integration.py | 10 | 99% |
| **Total** | **68** | **96%** |

### What the Tests Validate

- **Config loading**: YAML parsing, version mapping, JDK/JavaFX configuration
- **CLI argument parsing**: All options (--api, --version, --jdkversion) with valid/invalid inputs
- **Version resolution**: Valid versions map correctly, invalid versions fallback to latest
- **SDK context building**: All 4 supported JDKs (11, 17, 21, 25) map to correct JavaFX versions
- **API-specific behavior**: EMA vs ETA dependencies, JUnit scope, namespace resolution
- **pom.xml generation**: Valid XML output with correct properties and dependencies
- **End-to-end workflows**: Complete scenarios with various API/JDK combinations

## <a id="ref"></a>References

- [Real-Time SDK Java page](https://developers.lseg.com/en/api-catalog/real-time-opnsrc/rt-sdk-java) on the [LSEG Developers Community](https://developers.lseg.com/) website.
- [Real-Time SDK Family](https://developers.lseg.com/en/use-cases-catalog/real-time) page.
- [Apache Maven Project page](https://www.apache.org/)
- [Maven Getting Started Guide](https://maven.apache.org/guides/getting-started/)
- [Maven in 5 Minutes](https://maven.apache.org/guides/getting-started/maven-in-five-minutes.html)
- [Maven Central Repository Search](https://search.maven.org/)
- [Developer Article: How to Set Up Refinitiv Real-Time SDK Java Application with Maven](https://developers.lseg.com/en/article-catalog/article/how-to-set-up-refinitiv-real-time-sdk-java-application-with-mave).
- [Developer Article: How to deploy and run Real-Time Java Application with Maven in Docker](https://developers.lseg.com/en/article-catalog/article/how-to-deploy-and-run-real-time-java-application-with-maven-in-d).
- [How to Set Up Real-Time SDK Java Application with Maven on the Eclipse IDE](https://developers.lseg.com/en/article-catalog/article/how-to-set-up-real-time-sdk-java-application-with-maven-on-the-e) on the the [LSEG Developer Community](https://developers.lseg.com/) website.
- [JavaFX](https://gluonhq.com/products/javafx/) product website.