# ရွှေပန်းရွာ ခြံလေး — Android app

ဂိမ်းဖိုင် (`../shwe-pan-farm.html`) ကို build လုပ်ချိန် app ထဲ `index.html` အဖြစ် အလိုလို ကူးထည့်တယ်။ ဂိမ်းပြင်ရင် ဒီ folder ကို ထပ်ပြင်စရာ မလိုဘူး။

## Cloud build (GitHub Actions)
`shwe-pan-farm.html` ဒါမှမဟုတ် `android/` ပြောင်းပြီး push လုပ်တိုင်း **Actions → Android build** က အလိုလို build လုပ်တယ်:
- `shwe-pan-farm-debug-apk` — ဖုန်းမှာ တိုက်ရိုက် install လုပ်ပြီး စမ်းဖို့
- `shwe-pan-farm-release-aab` — Play Console ကို တင်ဖို့ (upload key secret ၄ ခု ထည့်ထားမှ sign လုပ်ပြီးသား ထွက်မယ်)

Repository → Settings → Secrets and variables → Actions:
`UPLOAD_KEYSTORE_BASE64`, `UPLOAD_STORE_PASSWORD`, `UPLOAD_KEY_ALIAS`, `UPLOAD_KEY_PASSWORD`
versionCode = Actions run number (တင်တိုင်း အလိုလို တိုးတယ်)။ versionName ကို `app/build.gradle.kts` မှာ ပြောင်းပါ။

## Android Studio
`android/` folder ကို ဖွင့် → Build → Generate Signed App Bundle။ ဒါမှမဟုတ် `android/keystore.properties` (git ထဲ မထည့်) ဖိုင်:
```
storeFile=/path/to/upload.jks
storePassword=...
keyAlias=upload
keyPassword=...
```

## ပါဝင်တာ
- WebView (offline, `appassets.androidplatform.net`), JavaScript + localStorage save
- Back ခလုတ် → `window.onAndroidBack()`; ဂိမ်းထဲ ထွက်ခလုတ် → `AndroidApp.quit()`
- Splash screen (နေကြာပန်း), adaptive icon, fullscreen, notch, screen-on, စာလုံးအရွယ် 100% ပုံသေ
- Permission: `VIBRATE` တစ်ခုတည်း (အင်တာနက် မလို)
- package `com.zay.shwepanfarm`, minSdk 24, targetSdk 35

## Play Store
`play-store/` — icon 512, feature graphic, screenshot ၆ ပုံ, privacy policy, listing စာ (`store-listing.md`)
