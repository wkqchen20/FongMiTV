package androidx.media3.exoplayer.libass;

/**
 * Stand-in for the JNI entry point that libmedia3ass.so resolves by binary name.
 *
 * <p>Only referenced by proguard-rules-media.pro, to keep the name intact for the native
 * library. With libass unavailable that library is never loaded, so an empty class is
 * enough to satisfy the keep rule and R8.
 */
public final class LibassNative {

    private LibassNative() {
    }
}
