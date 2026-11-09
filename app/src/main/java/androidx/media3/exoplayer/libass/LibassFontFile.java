package androidx.media3.exoplayer.libass;

import androidx.annotation.Nullable;

import java.io.File;
import java.io.IOException;

/**
 * Stand-in for the font metadata reader that FongMi/media does not publish.
 *
 * <p>Returns null, which makes ExternalFont.requireFamilyName raise "Font family name is
 * missing" and fails an external font import. Reading the font name table is a real
 * option (android.graphics.fonts.Font on API 29+) but is deliberately left out for now:
 * it would be new behaviour rather than a stub, and it would obscure whether the rest of
 * this substitution holds.
 *
 * <p>{@code throws IOException} is not decorative. ExternalFont.readFamilyName catches
 * IOException around this call, and in Java a catch block for a checked exception that
 * cannot be thrown is a compile error, so the declaration has to stay.
 */
@SuppressWarnings("unused")
public final class LibassFontFile {

    private LibassFontFile() {
    }

    @Nullable
    public static String getFamilyName(File file) throws IOException {
        return null;
    }
}
