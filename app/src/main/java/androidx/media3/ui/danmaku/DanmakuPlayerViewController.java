package androidx.media3.ui.danmaku;

import android.net.Uri;

import androidx.annotation.Nullable;
import androidx.media3.ui.PlayerView;

import okhttp3.OkHttpClient;

/**
 * Binds the danmaku controller of a {@link PlayerView} and forwards the controls that
 * PlaybackActivity drives it with.
 *
 * <p>This one is a real implementation, not a stand-in. FongMi/media publishes the whole
 * danmaku subsystem in its ui_danmaku module, and lib-ui-release.aar therefore ships a
 * PlayerView that already owns a DanmakuController, already wired to the DanmakuView in
 * exo_player_view.xml (id exo_danmaku) and already following the player through
 * setPlayer(). Only this facade was left unpublished, and every call it receives has a
 * public equivalent on PlayerView.
 *
 * <p>The setters are buffered because they arrive before the view does: PlaybackActivity
 * .configurePlayerView() runs from initView, while bind() is called later, from
 * syncPlayerView(), once the playback service has connected. Replaying them on bind is
 * what keeps the HTTP client, the configuration and the enabled flag from being lost.
 */
public final class DanmakuPlayerViewController {

    @Nullable private PlayerView playerView;
    @Nullable private OkHttpClient okHttpClient;
    @Nullable private DanmakuConfig config;
    @Nullable private Uri dataSource;
    private boolean enabled;
    private boolean enabledSet;

    /**
     * Points subsequent calls at {@code newPlayerView}'s danmaku controller.
     *
     * <p>Re-binding the same view is a no-op: syncPlayerView() runs again on every player
     * rebuild, and replaying the source each time would restart the danmaku fetch for no
     * reason. A null view only clears the reference; the controller itself belongs to the
     * PlayerView.
     */
    public void bind(@Nullable PlayerView newPlayerView) {
        if (playerView == newPlayerView) return;
        playerView = newPlayerView;
        if (newPlayerView == null) return;
        if (okHttpClient != null) newPlayerView.setDanmakuOkHttpClient(okHttpClient);
        if (enabledSet) newPlayerView.setDanmakuEnabled(enabled);
        if (config != null) newPlayerView.setDanmakuConfig(config);
        if (dataSource != null) newPlayerView.setDanmakuSource(dataSource);
    }

    public void setOkHttpClient(@Nullable OkHttpClient client) {
        okHttpClient = client;
        if (playerView != null) playerView.setDanmakuOkHttpClient(client);
    }

    public void setDataSource(@Nullable Uri uri) {
        dataSource = uri;
        if (playerView != null) playerView.setDanmakuSource(uri);
    }

    public void setConfig(DanmakuConfig config) {
        this.config = config;
        if (playerView != null) playerView.setDanmakuConfig(config);
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
        this.enabledSet = true;
        if (playerView != null) playerView.setDanmakuEnabled(enabled);
    }

    public void sendNow(String text) {
        if (playerView != null) playerView.sendDanmaku(text);
    }

    /**
     * Drops the reference without touching the controller. The PlayerView owns it and
     * tears it down on its own in setPlayer(null), which PlaybackActivity reaches through
     * detachPlayerView() one line earlier.
     */
    public void close() {
        playerView = null;
    }
}
