// Ghidra post-script: export discovered functions to CSV.
import java.io.File;
import java.io.PrintWriter;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.address.Address;

public class ExportFunctions extends GhidraScript {
    public void run() throws Exception {
        String path = getScriptArgs().length > 0 ? getScriptArgs()[0] : "functions.csv";
        File outFile = new File(path);
        File parent = outFile.getParentFile();
        if (parent != null) parent.mkdirs();
        try (PrintWriter out = new PrintWriter(outFile, "UTF-8")) {
            out.println("program,name,entry_address,body_min,body_max,size,thunk,external");
            FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
            while (it.hasNext()) {
                Function f = it.next();
                Address entry = f.getEntryPoint();
                Address min = f.getBody().getMinAddress();
                Address max = f.getBody().getMaxAddress();
                out.printf("\"%s\",\"%s\",%s,%s,%s,%d,%s,%s%n",
                    csv(currentProgram.getName()), csv(f.getName()),
                    entry, min, max, f.getBody().getNumAddresses(),
                    f.isThunk(), f.isExternal());
            }
        }
        println("Wrote function export: " + outFile.getAbsolutePath());
    }
    private String csv(String s) {
        return s == null ? "" : s.replace("\"", "\"\"");
    }
}
