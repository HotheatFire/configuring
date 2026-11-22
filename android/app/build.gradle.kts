import java.util.Properties

plugins {
    id("com.android.application")
}

// Release signing: keystore.properties (local, not in git) or environment variables (cloud build).
val keyProps = Properties().apply {
    val f = rootProject.file("keystore.properties")
    if (f.exists()) f.inputStream().use { load(it) }
}
fun signingValue(key: String, env: String): String? =
    (keyProps.getProperty(key) ?: System.getenv(env))?.takeIf { it.isNotBlank() }

val storeFilePath = signingValue("storeFile", "SIGNING_STORE_FILE")

android {
    namespace = "com.zay.shwepanfarm"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.zay.shwepanfarm"
        minSdk = 24
        targetSdk = 35
        versionCode = (System.getenv("VERSION_CODE") ?: "1").toInt()
        versionName = "1.0"
    }

    signingConfigs {
        if (storeFilePath != null) {
            create("release") {
                storeFile = file(storeFilePath)
                storePassword = signingValue("storePassword", "SIGNING_STORE_PASSWORD")
                keyAlias = signingValue("keyAlias", "SIGNING_KEY_ALIAS")
                keyPassword = signingValue("keyPassword", "SIGNING_KEY_PASSWORD")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            if (storeFilePath != null) signingConfig = signingConfigs.getByName("release")
        }
    }

    buildFeatures {
        buildConfig = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

// The game itself lives at the repo root (shwe-pan-farm.html); it is copied into the app as index.html at build time.
abstract class CopyGameTask : DefaultTask() {
    @get:InputFile
    abstract val game: RegularFileProperty

    @get:OutputDirectory
    abstract val outputDir: DirectoryProperty

    @TaskAction
    fun copy() {
        val out = outputDir.get().asFile
        out.mkdirs()
        game.get().asFile.copyTo(File(out, "index.html"), overwrite = true)
    }
}

val copyGame = tasks.register<CopyGameTask>("copyGame") {
    game.set(rootProject.layout.projectDirectory.file("../shwe-pan-farm.html"))
}

androidComponents {
    onVariants { variant ->
        variant.sources.assets?.addGeneratedSourceDirectory(copyGame, CopyGameTask::outputDir)
    }
}

dependencies {
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("androidx.core:core:1.13.1")
    implementation("androidx.core:core-splashscreen:1.0.1")
    implementation("androidx.webkit:webkit:1.12.1")
}
